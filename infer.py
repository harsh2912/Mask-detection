from flask import Flask,jsonify,request,send_from_directory
from flask_cors import CORS
import base64
import os
import argparse
from model import Model


retina_path = './Face_detection/models/retinaface/R50'
req_add = 'http://127.0.0.1:3000/'


if __name__ == "__main__":
    
    model = Model(retina_path,req_add)

    
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--is_image',type=bool,default=False)
    parser.add_argument('--in_path', type=str)
    parser.add_argument('--out_path',type=str)
    args = parser.parse_args()
    
    if args.is_image:
        type_ = 'image'
    else:
        type_ = 'video'
    model.generate_output(args.in_path,args.out_path,type_)
        