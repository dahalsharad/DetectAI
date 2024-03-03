import os
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import numpy as np
import joblib,os
from flask import Flask, render_template, request
from pathlib import Path

import numpy as np
import tensorflow as tf


import PyPDF2
import docx2txt
from spire.doc import *
from spire.doc.common import *

import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import keras


BASE_DIR = Path(__file__).resolve().parent.parent
####### requirements for predict_text function ############
# Model accuracies (GB, LR, MLP, RF)
accuracy = [0.875, 0.675, 0.7, 0.915]
# Output Labels
label = ["AI GENERATED", "HUMAN WRITTEN", "INCONCLUSIVE"]
# # normalization of accuracy to obtain weight
# sum_accuracy = sum(accuracy)
# weight  = [val / sum_accuracy for val in accuracy]
# print(weight)

weight = [0.2764612954186414, 0.2132701421800948, 0.22116903633491308, 0.2890995260663507]
# Load the saved models
tfidf_vectorizer = joblib.load('./models/tfidf_vectorizer.pkl')
RF = joblib.load('./models/RF_model.pkl')
GB = joblib.load('./models/GB_model.pkl')
MLP = joblib.load('./models/MLP_model.pkl')
LR = joblib.load('./models/LR_model.pkl')
############################################################

image_label = ["AI GENERATED", "REAL", "INCONCLUSIVE"]

def predict_text(random_text):

        # Transform the new text using the loaded TF-IDF vectorizer
        random_text_tfidf = tfidf_vectorizer.transform([random_text])


        prediction = [0, 0, 0, 0]

        # Make predictions using the loaded classifier
        pred = GB.predict(random_text_tfidf)
        pred = pred [0]
        if pred == 1:
            prediction[0] = 1
        
        pred = LR.predict(random_text_tfidf)
        pred = pred [0]
        if pred == 1:
            prediction[1] = 1
        
        pred = MLP.predict(random_text_tfidf)
        pred = pred [0]
        if pred == 1:
            prediction[2] = 1

        pred = RF.predict(random_text_tfidf)
        pred = pred [0]
        if pred == 1:
            prediction[3] = 1

        # Weighted voting for binary predictions (0 or 1)
        weighted_prediction = sum(weight * prediction for weight, prediction in zip(weight, prediction))

        # Choosing the label based on the weighted sum
        if weighted_prediction > 0.5 :
            final_prediction = label[0]
            confidence = int(100*round(weighted_prediction,2))
        elif weighted_prediction < 0.5 :
            final_prediction = label[1]
            confidence = int(100*round((1 - weighted_prediction),2))
        else:
            final_prediction = label[2]
            confidence = 0
        
        return random_text,prediction,confidence,final_prediction



def store_file(file, extension):
    with open("uploads/files/temp"+extension, "wb+") as dest:
        for chunk in file.chunks():
            dest.write(chunk)



def read_file(extension):
    text = ""
    if extension==".pdf":
        pdfFileObj = open('uploads/files/temp.pdf', 'rb')

        # creating a pdf reader object
        pdfReader = PyPDF2.PdfReader(pdfFileObj)

        # printing number of pages in pdf file
        print(len(pdfReader.pages))

        # creating a page object
        pageObj = pdfReader.pages[0]

        # extracting text from page
        text = pageObj.extract_text()

        # closing the pdf file object
        pdfFileObj.close()

    
    elif extension==".txt":
        with open('uploads/files/temp.txt', 'r') as file:
            text = file.read()

    elif extension==".docx":
        text = docx2txt.process("uploads/files/temp.docx")

    elif extension ==".doc":
        document = Document()
        document.LoadFromFile("uploads/files/temp.doc")
        document.SaveToFile("uploads/files/t.docx", FileFormat.Docx2016)
        document.Close()
        text = docx2txt.process("uploads/files/t.docx")
        text = text.replace("Evaluation Warning: The document was created with Spire.Doc for Python.", "")
        os.remove("uploads/files/t.docx")

    return(text)

def store_image(image, image_name):
    with open("aidetector/static/image/"+image_name, "wb+") as dest:
        for chunk in image.chunks():
            dest.write(chunk)


#create the image detection model's architecture and compile it
def get_model(input_shape):

    input = tf.keras.Input(shape=input_shape)

    densenet = tf.keras.applications.DenseNet121( weights="imagenet", include_top=False, input_tensor = input)

    x = tf.keras.layers.GlobalAveragePooling2D()(densenet.output)
    x = tf.keras.layers.Dense(512, activation='relu')(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Dropout(0.3)(x)
    output = tf.keras.layers.Dense(1, activation='sigmoid')(x) #binary classification

    model = tf.keras.Model(densenet.input, output)

    model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])

    return model

input_shape = (256, 256, 3)
model = get_model(input_shape)
model.load_weights('./models/model_cp.h5')

def predict_image(name):
    print(name)
    test_image = tf.keras.preprocessing.image.load_img(name, target_size=(256, 256, 3))


    test_image_arr = tf.keras.preprocessing.image.img_to_array(test_image)
    test_image_arr = np.expand_dims(test_image, axis=0)
    test_image_arr = test_image_arr/255.


    result = model.predict(test_image_arr)
    result = result[0][0]
    if result > 0.5 :
        final_prediction = image_label[1]
        confidence = int(100*round(result,2))
    elif result < 0.5 :
        final_prediction = image_label[0]
        confidence = int(100*round((1 - result),2))
    else:
        final_prediction = image_label[2]
        confidence = 0
    return name, confidence, final_prediction


########################
# image heatmap
########################

def save_and_display_gradcam(img_path, heatmap, cam_path="cam.jpg", alpha=0.9):
    # Load the original image
    cam_path = "aidetector/static/image_heatmap.jpg"
    img = keras.utils.load_img(img_path)
    img = keras.utils.img_to_array(img)

    # Rescale heatmap to a range 0-255
    heatmap = np.uint8(255 * heatmap)

    # Use jet colormap to colorize heatmap
    jet = cm.get_cmap("jet")

    # Use RGB values of the colormap
    jet_colors = jet(np.arange(256))[:, :3]
    jet_heatmap = jet_colors[heatmap]

    # Create an image with RGB colorized heatmap
    jet_heatmap = keras.utils.array_to_img(jet_heatmap)
    jet_heatmap = jet_heatmap.resize((img.shape[1], img.shape[0]))
    jet_heatmap = keras.utils.img_to_array(jet_heatmap)

    # Superimpose the heatmap on original image
    superimposed_img = jet_heatmap * alpha + img
    superimposed_img = keras.utils.array_to_img(superimposed_img)

    # Save the superimposed image
    superimposed_img.save(cam_path)

def make_gradcam_heatmap(img_array, model, last_conv_layer_name, pred_index=None):
    # First, we create a model that maps the input image to the activations
    # of the last conv layer as well as the output predictions
    grad_model = keras.models.Model(
        model.inputs, [model.get_layer(last_conv_layer_name).output, model.output]
    )

    # Then, we compute the gradient of the top predicted class for our input image
    # with respect to the activations of the last conv layer
    with tf.GradientTape() as tape:
        last_conv_layer_output, preds = grad_model(img_array)
        if pred_index is None:
            pred_index = tf.argmax(preds[0])
        class_channel = preds[:, pred_index]

    # This is the gradient of the output neuron (top predicted or chosen)
    # with regard to the output feature map of the last conv layer
    grads = tape.gradient(class_channel, last_conv_layer_output)

    # This is a vector where each entry is the mean intensity of the gradient
    # over a specific feature map channel
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    # We multiply each channel in the feature map array
    # by "how important this channel is" with regard to the top predicted class
    # then sum all the channels to obtain the heatmap class activation
    last_conv_layer_output = last_conv_layer_output[0]
    heatmap = last_conv_layer_output @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)

    # For visualization purpose, we will also normalize the heatmap between 0 & 1
    heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
    return heatmap.numpy()


def image_heatmap_generator(img_path):

    test_image = tf.keras.preprocessing.image.load_img(img_path, target_size=(256, 256, 3))
    img = tf.keras.preprocessing.image.img_to_array(test_image)
    img = np.expand_dims(img, axis=0)
    img = img/255.

    # Generate class activation heatmaps
    heatmap_1 = make_gradcam_heatmap(img, model, "conv5_block16_1_conv")
    # heatmap_2 = make_gradcam_heatmap(img, model, "conv5_block16_2_conv")
    # heatmap_3 = make_gradcam_heatmap(img, model, "conv5_block15_1_conv")
    # heatmap_4 = make_gradcam_heatmap(img, model, "conv5_block14_1_conv")
    # heatmap_5 = make_gradcam_heatmap(img, model, "conv5_block13_2_conv")

    # Merge heatmaps
    # merged_heatmap = (heatmap_1 + heatmap_2 ) / 3.0



    save_and_display_gradcam(img_path, heatmap_1)