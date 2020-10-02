from flask import Flask,jsonify
from flask import render_template,request, redirect,render_template_string
from flask_cors import CORS
import sqlite3
import datetime as dt
import io
import numpy as np
import pandas as pd
from mask_check import maskModel
from PIL import Image
import base64
import pickle

app = Flask(__name__)
CORS(app)

req_add = 'http://127.0.0.1:3000/'
device = 'cuda'
model = maskModel(device)


def base642np(base64_str):
    base64_str = str(base64_str).replace('data:image/jpeg;base64,', '')
    image = Image.open(io.BytesIO(base64.b64decode(base64_str))).convert('RGB')
    #image.save('sdjfsd.jpg')
    return np.array(image)


@app.route("/", methods=["POST"])
def index():
    if request.method == "POST":
        faces=pickle.loads(request.get_data())
#         faces=data.get('faces',None)
#         faces = joblib.loads(faces)
        img_arr = np.array(faces)
        print('here')
        out = model.check_mask(img_arr)
        #print('request_receieved')
        return jsonify({'result':out})

if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)