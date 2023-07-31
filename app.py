import os
import numpy as np
import flask
import pickle
from flask import Flask, render_template, request

app = Flask(__name__, template_folder='templates')

@app.route('/')
def student():
    return render_template("index.html")

def ValuePredictor(to_predict_list):
    if len(to_predict_list) != 11:
        # Handle the case where the input list doesn't have 11 elements
        return "Error: Input list must contain 11 elements."

    to_predict = np.array(to_predict_list).reshape(1, 11)
    load_model = pickle.load(open("modelsvm.pkl", "rb"))
    result = load_model.predict(to_predict)
    return round(result[0], 2)

@app.route('/', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        to_predict_list = request.form.to_dict()
        to_predict_list = list(to_predict_list.values())
        to_predict_list = list(map(float, to_predict_list))
        if len(to_predict_list) != 11:
            # Render an error message if the input list doesn't have 11 elements
            return render_template("index.html", result_text='Error: Input must contain 11 values.')
        
        result = float(ValuePredictor(to_predict_list))
        return render_template("hasil.html", result_text='Prediksi Hasil Panen Anda :  {}  Ton '.format(result))

if __name__ == '__main__':
    app.run(debug=True)
