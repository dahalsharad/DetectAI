import csv
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import numpy as np
import joblib
from flask import Flask, render_template, request

weight = [0.2764612954186414, 0.2132701421800948, 0.22116903633491308, 0.2890995260663507]

# Load the saved models
loaded_tfidf_vectorizer = joblib.load('tfidf_vectorizer.pkl')
RF = joblib.load('RF_model.pkl')
GB = joblib.load('GB_model.pkl')
LSVC = joblib.load('LSVC_model.pkl')
MLP = joblib.load('MLP_model.pkl')
LR = joblib.load('LR_model.pkl')

def predict(random_text):

        # Transform the new text using the loaded TF-IDF vectorizer
        random_text_tfidf = loaded_tfidf_vectorizer.transform([random_text])

        prediction = [0, 0, 0, 0, 0]

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
        final_prediction = 1 if weighted_prediction > 0.5 else 0
        if weighted_prediction > 0.5 :
            final_prediction = 1
        elif weighted_prediction < 0.5 :
            final_prediction = 0
        else:
            final_prediction = 2

        return weighted_prediction,final_prediction
        

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def prediction():
    if request.method == 'POST':
        text = request.form['input_text']
        confidence, prediction = predict(text)
        if prediction == 1:
            result = "AI GENERATED"
        elif prediction == 2:
            result = "INCONCLUSIVE"
        else:
            confidence = 1 - confidence
            result = "HUMAN WRITTEN"
        return render_template('predict.html', input_text=text, result=result, confidence=confidence)

if __name__ == '__main__':
    app.run(debug=True)
