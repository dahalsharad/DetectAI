import pytesseract, threading
import cv2, os
import numpy as np
from .utils import predict_text
confidence_temp = []


def highlight_regions(regions,image_path,filename):
    
    transparency = 0.5
    # Load the imageos.path.join(image_directory, f
    image = cv2.imread(image_path)


    if not os.path.exists("uploads/highlight"):
        os.makedirs("uploads/highlight")
    

    # Convert transparency to alpha value
    alpha = transparency * 255

    # Iterate over regions and draw translucent red rectangles
    for row in regions:
        for region in row:
            left = region['l']
            top = region['t']
            width = region['w']
            height = region['h']

            # Create a mask for the region
            mask = np.zeros_like(image[:, :, 0])
            mask[top:top+height, left:left+width] = 255

            # Apply Gaussian blur to the mask to make it translucent
            blurred_mask = cv2.GaussianBlur(mask, (25, 25), 0)

            # Apply the mask to the image
            highlighted_image = image.copy()
            highlighted_image[blurred_mask != 0] = (0, 255, 255)  # Red highlight color (BGR format)

            # Merge the highlighted image with the original image using alpha blending
            cv2.addWeighted(highlighted_image, transparency, image, 1 - transparency, 0, image)

    # Save the highlighted image as PNG
    cv2.imwrite("uploads/highlight/"+filename+"_highlighted.png", image)




def process_text(sentence_text, words_info):
    random_text,prediction,confidence,final_prediction = predict_text(sentence_text)
    if final_prediction != "AI GENERATED":
        confidence = 100 - confidence
    confidence_temp.append(confidence)
    positive_val = []
    
    if confidence > 50:
        for word_info in words_info:
            positive_val.append({
                'l': word_info['left'],
                't': word_info['top'],
                'w': word_info['width'],
                'h': word_info['height']
            })
    
    return confidence, positive_val

# Function to calculate the average height of words
def average_word_height(words):
    total_height = sum(word['height'] for word in words)
    return total_height / len(words) if len(words) > 0 else 0

# Function to check if two words are in the same sentence
def are_words_in_same_sentence(word1, word2, avg_height, threshold_factor=1.5):
    threshold = threshold_factor * avg_height
    return abs(word1['top'] - word2['top']) <= threshold

def ocr(image_path, filename, heatmap):
    positive_val_all = []
    
    # Perform OCR on the image
    image = cv2.imread(image_path)
    text = pytesseract.image_to_string(image)
    d = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    
    # Initialize sentences list
    sentences = []
    current_sentence = []
    
    # Calculate average word height
    avg_height = average_word_height([{'height': h} for h in d['height']])
    
    # Iterate through each word detected by OCR
    for i_word, word in enumerate(d['text']):
        if word:
            word_info = {
                'text': word.strip(),
                'left': d['left'][i_word],
                'top': d['top'][i_word],
                'width': d['width'][i_word],
                'height': d['height'][i_word]
            }
            if current_sentence and not are_words_in_same_sentence(current_sentence[-1], word_info, avg_height):
                sentence_text = ' '.join(word_info['text'] for word_info in current_sentence)
                sentences.append({
                    'sentence': sentence_text,
                    'words': current_sentence.copy()
                })
                current_sentence = []
            current_sentence.append(word_info)
    
    if current_sentence:
        sentence_text = ' '.join(word_info['text'] for word_info in current_sentence)
        sentences.append({
            'sentence': sentence_text,
            'words': current_sentence.copy()
        })

    # Initialize list to store merged sentences
    merged_sentences = []
    current_merged_sentence = ""
    current_words = []

    # Iterate through each sentence
    for sentence in sentences:
        current_merged_sentence += " " + sentence['sentence']
        current_words.extend(sentence['words'])

        # Check if adding the current sentence exceeds the maximum length of 200 words
        while len(current_words) >= 200:
            merged_sentences.append({
                'sentence': current_merged_sentence.strip(),
                'words': current_words[:200].copy()
            })
            del current_words[:200]
            current_merged_sentence = ' '.join(word_info['text'] for word_info in current_words)

    if current_merged_sentence:
        merged_sentences.append({
            'sentence': current_merged_sentence.strip(),
            'words': current_words.copy()
        })

    for sentence in merged_sentences:
        confidence, positive_val = process_text(sentence['sentence'], sentence['words'])
        if confidence > 50:
            positive_val_all.append(positive_val)


    if heatmap == 1:
        thread = threading.Thread(target=highlight_regions(positive_val_all,image_path, filename))
        thread.start()

def start_img_processing(heatmap):
    
    for filename in os.listdir("uploads/temp/output"):
    # Check if the file is an image file
        if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.jpeg'):
            filepath = "uploads/temp/output/" + filename
            ocr(filepath ,filename, heatmap)


    greater_than_50_count = sum(1 for num in confidence_temp if num > 50)
    less_than_50_count = sum(1 for num in confidence_temp if num < 50)
    greater_than_50_sum = sum(num for num in confidence_temp if num > 50)
    less_than_50_sum = sum(num for num in confidence_temp if num < 50)

    # Calculating averages for each category, handling division by zero
    greater_than_50_avg = greater_than_50_sum / greater_than_50_count if greater_than_50_count > 0 else 0
    less_than_50_avg = less_than_50_sum / less_than_50_count if less_than_50_count > 0 else 0


    if greater_than_50_count >= less_than_50_count:
        document_authenticity = "AI GENERATED"
        final_confidence = greater_than_50_avg
    else:
        document_authenticity = "HUMAN WRITTEN"
        final_confidence = 100 - less_than_50_avg
    return document_authenticity,final_confidence