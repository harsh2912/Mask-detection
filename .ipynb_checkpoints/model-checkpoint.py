from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from scipy import misc
import sys
import os
import argparse
#import tensorflow as tf
import numpy as np
import mxnet as mx
from glob import glob
import random
import cv2
import sklearn
from sklearn.decomposition import PCA
from time import sleep
from easydict import EasyDict as edict
# from mtcnn_detector import MtcnnDetector
sys.path.append(os.path.join('./Face_detection', 'src', 'common'))
import face_image
import face_preprocess
sys.path.append('./Face_detection')
sys.path.append('./Face_detection/RetinaFace/')
from RetinaFace.retinaface import RetinaFace
import time
import random
import matplotlib.pyplot as plt
import base64
import requests
from PIL import Image
import base64
from io import BytesIO
import imutils
import pickle

def get_padded_image(img):
    dim = np.argmax(img.shape[:2])
    arr = np.zeros((250,250,3),dtype='uint8')
    if dim == 1:
        resized_image = imutils.resize(img,width=250)
        half = int((250-resized_image.shape[0])/2)
        h = resized_image.shape[0]
        arr[half:half+h,:] = resized_image
    else:
        resized_image = imutils.resize(img,height=250)
        half = int((250-resized_image.shape[1])/2)
        w = resized_image.shape[1]
        arr[:,half:half+w,:] = resized_image
    return arr


class Model:
    def __init__(self,retina_path,request_add,det_threshold=0.8):
        self.detector = RetinaFace(retina_path,0, ctx_id=0)
        self.request_add = request_add
        self.det_threshold = det_threshold
        
    def check_mask(self,encoded_image):
        r = requests.post(self.request_add,data=encoded_image)
        result = r.json()['result']
        return result
    
    
    def get_face_patch(self,img):
        bboxes,points = self.detector.detect(img, self.det_threshold,scales=[1.0],do_flip=False)
        faces_=[]
        key_points_=[]
        bboxes_=[]
        for face,point in zip(bboxes,points):
            #import pdb; pdb.set_trace()
            bbox = face[0:4].astype(np.int)
            to_add_face=img[bbox[1]:bbox[3],bbox[0]:bbox[2]]
            to_add_face = get_padded_image(to_add_face)[...,::-1]/255.0
           # print(to_add_face.shape)
            faces_.append(to_add_face)
            key_points_.append((points.astype(np.int),face[4]))
            bboxes_.append(bbox)
            #print(to_add_face.shape)

        return np.array(faces_),np.array(key_points_),np.array(bboxes_)
    
    def generate_output(self,read_path,write_path,type_='video'):
        if type_ == 'video':
            self.generate_video(read_path,write_path)
        else:
            self.generate_image(read_path,write_path)
        
        
    def generate_video(self,read_path,write_path):
        cap = cv2.VideoCapture(read_path)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        fps = cap.get(cv2.CAP_PROP_FPS)
        ret , fr = cap.read()
        org_h,org_w = fr.shape[:2]
        out = cv2.VideoWriter(f'{write_path}', fourcc, fps, (org_w,org_h))
        counter = 0
        while ret:
            if counter%2 == 0:
                counter = 0
                fr = self._infer_on_frame(fr)
                out.write(fr)
                ret,fr = cap.read()
            counter += 1
        out.release()
        
    def generate_image(self,read_path,write_path):
        fr = cv2.imread(read_path)
        if fr is None:
            print('Invalid Image')
            return
        fr = self._infer_on_frame(fr)
        plt.imsave(write_path,fr[:,:,::-1])
        
    def _infer_on_frame(self,fr):
#         org_h,org_w = fr.shape[:2]
#         fr = imutils.resize(fr,width=720)
        faces , keypoints , bboxes = self.get_face_patch(fr)
        if not len(faces)==0:s
            encoded_arr = pickle.dumps(faces)
            output = self.check_mask(encoded_arr)
            
            for out,bbox in zip(output,bboxes):
#             for bbox in bboxes:
                x1,y1,x2,y2 = bbox
                if out == 'mask':
                    color = (0,255,0)
                else:
                    color = (0,0,255)
                #color = (0,255,0)
                fr = cv2.rectangle(fr.copy(),(x1,y1),(x2,y2),color,2)
#         fr = cv2.resize(fr.copy(),(org_w,org_h))
        return fr