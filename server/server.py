# server.py
import csv
import copy
import itertools
import cv2
import mediapipe as mp
from dotenv import load_dotenv
import os

from model import KeyPointClassifier
from flask import Flask, request, jsonify

# Automatically load .env file in the current directory
load_dotenv()

# Get the server name from environment variables
PORT = os.getenv("PORT")

app = Flask(__name__)


def calc_landmark_list(image, landmarks):
    
    # Calculate pixel coordinates of hand landmarks from normalized values
    image_width, image_height = image.shape[1], image.shape[0]
    landmark_point = []

    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)
        # landmark_z = landmark.z

        landmark_point.append([landmark_x, landmark_y])

    return landmark_point


def pre_process_landmark(landmark_list):
    # Converting absolute coordinates to relative, normalization, and flattening the list
    temp_landmark_list = copy.deepcopy(landmark_list)

    # Convert to relative coordinates by setting wrist landmark coordinate as origin
    base_x, base_y = 0, 0
    for index, landmark_point in enumerate(temp_landmark_list):
        if index == 0:
            base_x, base_y = landmark_point[0], landmark_point[1]

        temp_landmark_list[index][0] = temp_landmark_list[index][0] - base_x
        temp_landmark_list[index][1] = temp_landmark_list[index][1] - base_y

    # Flatten to a 1D list
    temp_landmark_list = list(
        itertools.chain.from_iterable(temp_landmark_list))

    # Normalization
    max_value = max(list(map(abs, temp_landmark_list)))

    def normalize_(n):
        return n / max_value

    temp_landmark_list = list(map(normalize_, temp_landmark_list))
    return temp_landmark_list

# Initialize the model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)

# Load
keypoint_classifier = KeyPointClassifier()

# Read Hand Gesture labels from CSV file
with open('model/keypoint_classifier/keypoint_classifier_label.csv', encoding='utf-8-sig') as f:
    keypoint_classifier_labels = csv.reader(f)
    keypoint_classifier_labels = [row[0] for row in keypoint_classifier_labels]


@app.route('/process', methods=['POST'])
def process_image():
    rec_img = request.files['img']

    # Save the image
    rec_img.save("received_image.jpg") 

    # Read image sent by the raspberry pi
    image = cv2.imread("received_image.jpg")
    print(image.shape)
    if image is None:
        print("Image Not Found!")
    image = cv2.flip(image, 1)  # Mirror display
    debug_image = copy.deepcopy(image)

    # Convert BGR frame to RGB frame to use with MediaPipe
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)    

    # Performance boost by disabling writing before processing
    image.flags.writeable = False
    results = hands.process(image)
    image.flags.writeable = True

    # Processes the image to detect hand landmarks, classify gestures, and return result 
    hand_sign_text = None
    if results.multi_hand_landmarks is not None:
        for hand_landmarks in (results.multi_hand_landmarks):
            # Landmark calculation
            landmark_list = calc_landmark_list(debug_image, hand_landmarks)

            # Conversion to relative coordinates / normalized coordinates
            pre_processed_landmark_list = pre_process_landmark(
                landmark_list)

            # Hand sign classification
            hand_sign_id = keypoint_classifier(pre_processed_landmark_list)
            hand_sign_text = keypoint_classifier_labels[hand_sign_id]

            # Print statement for server side monitoring
            print(f"The Hand sign shown is: {hand_sign_text}")

    print("[+] Received image and processed it")
    return jsonify({'result': hand_sign_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)