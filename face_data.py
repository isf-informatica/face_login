import cv2
import face_recognition
import numpy as np
from flask import Flask, render_template, request,jsonify
import os
# from app1 import known_faces_encoding,known_faces_names

upendra=face_recognition.load_image_file('labeled/upendra/9.png')
rahul=face_recognition.load_image_file('labeled/rahul/107.png')
sid=face_recognition.load_image_file('labeled/sid/73.jpg')
suraj=face_recognition.load_image_file('labeled/suraj/54.png')
andrew=face_recognition.load_image_file('labeled/andrew/47.png')

upendra_encode=face_recognition.face_encodings(upendra)[0]
rahul_encode=face_recognition.face_encodings(rahul)[0]
sid_encode=face_recognition.face_encodings(sid)[0]
suraj_encode=face_recognition.face_encodings(suraj)[0]
andrew_encode=face_recognition.face_encodings(andrew)[0]


# Predefined list of known faces and their names
known_faces_encoding=[
    upendra_encode,
    rahul_encode,
    sid_encode,
    suraj_encode,
    # rahul_marketing_encoding,
    andrew_encode
]

known_faces_names=[
    'upendra',
    'rahul',
    'sid',
    'suraj',
    # 'rahul_marketing',
    'andrew'
]



known_faces_encoding1=[]
known_faces_names1=[]

def face_register(name,dataUrl):
    if name in known_faces_names1:
        # break
        return print('Name already taken')
    else:
        a=face_recognition.load_image_file(dataUrl)
        b=face_recognition.face_encodings(a)[0]
        known_faces_encoding1.append(b)
        known_faces_names1.append(name)
        return 'Name Successfully Registerd'
    

