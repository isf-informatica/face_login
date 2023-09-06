import cv2
import face_recognition
import numpy as np
from flask import Flask, render_template, request, jsonify
import base64
import os
from win32com.client import Dispatch
from face_data import known_faces_encoding,known_faces_names

app = Flask(__name__)
app.static_folder = 'templates'

facedetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


def speak(str1):
    speak=Dispatch(("SAPI.SpVoice"))
    speak.Speak(str1)

def decode_base64_img(data_url):
    img_data = data_url.split(',')[1].encode('utf-8')
    with open('temp.png', 'wb') as f:
        f.write(base64.decodebytes(img_data))

my_name=[]

# Route for processing the photo and performing face recognition
@app.route('/process_photo', methods=['POST'])
def process_photo():
    if request.method == 'POST':
        data_url = request.get_json().get('imageData')  # Access the imageData from JSON

        if data_url:
            decode_base64_img(data_url)

            # Perform face recognition on the saved image
            frame = cv2.imread('temp.png')
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face=facedetect.detectMultiScale(gray,1.3,5)
            small_frame = cv2.resize(frame, (0, 0), fx=0.50, fy=0.50)
            
            face_locations = face_recognition.face_locations(small_frame)
            face_encodings = face_recognition.face_encodings(small_frame, face_locations)
            face_names = []
            recognized_known_face = False

            for face_encode in face_encodings:
                face_distances = face_recognition.face_distance(known_faces_encoding, face_encode)
                best_match_index = np.argmin(face_distances)
                confidence_threshold = 0.4

                if face_distances[best_match_index] < confidence_threshold:
                    name = known_faces_names[best_match_index]
                    recognized_known_face = True
                else:
                    name = "Unknown"

                face_names.append(name)

            # Clean up the temporary image
            os.remove('temp.png')

            # If any known faces are detected with high confidence, return success and the recognized name
            if recognized_known_face:
                recognized_name = next((name for name in face_names if name in known_faces_names), None)
                my_name.append(recognized_name)
                speak('Welcome'+' '+name)
                return jsonify(success=True, recognized_name=recognized_name)

    return jsonify(success=False)  # If no imageData or POST request, return failure


# Route for the main login page
@app.route('/')
def welcome():
    return render_template('page.html')

@app.route('/result') 
def result():
    return render_template('result.html',names=my_name)

@app.route('/signin')
def signin():
    my_name.clear()
    return render_template('page.html')
if __name__ == '__main__':
    app.run(debug=True)