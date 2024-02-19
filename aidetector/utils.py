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

        print(random_text_tfidf)

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
