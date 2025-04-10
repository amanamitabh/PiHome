#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import copy
import itertools
import time
import cv2 as cv
import numpy as np
import mediapipe as mp

from model import KeyPointClassifier


def main():

    # Load the model
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        max_num_hands=1
    )

    keypoint_classifier = KeyPointClassifier()
    # Read Hand Gesture labels from CSV file
    with open('model/keypoint_classifier/keypoint_classifier_label.csv', encoding='utf-8-sig') as f:
        keypoint_classifier_labels = csv.reader(f)
        keypoint_classifier_labels = [row[0] for row in keypoint_classifier_labels]

    while True:

        # Read image sent by the raspberry pi
        image = cv.imread("image3.jpg")
        if image is None:
            print("Image Not Found!")
            break
        image = cv.flip(image, 1)  # Mirror display
        debug_image = copy.deepcopy(image)


        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)    # Convert BGR frame to RGB frame to use with MediaPipe

        # Performance boost by disabling writing before processing
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True

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

                print(f"The Hand sign shown is: {hand_sign_text}")
                if hand_sign_id == 0:
                    # for Open Hand
                    print()

                elif hand_sign_id == 1:
                    # for Closed Hand
                    print()

                elif hand_sign_id == 2:
                    # for Pointed Hand
                    print()

                elif hand_sign_id == 3:
                    # for OK
                    print()

        # Screen reflection #############################################################
        time.sleep(2)




def calc_landmark_list(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]

    landmark_point = []

    # Keypoint
    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)
        # landmark_z = landmark.z

        landmark_point.append([landmark_x, landmark_y])

    return landmark_point


def pre_process_landmark(landmark_list):
    temp_landmark_list = copy.deepcopy(landmark_list)

    # Convert to relative coordinates
    base_x, base_y = 0, 0
    for index, landmark_point in enumerate(temp_landmark_list):
        if index == 0:
            base_x, base_y = landmark_point[0], landmark_point[1]

        temp_landmark_list[index][0] = temp_landmark_list[index][0] - base_x
        temp_landmark_list[index][1] = temp_landmark_list[index][1] - base_y

    # Convert to a one-dimensional list
    temp_landmark_list = list(
        itertools.chain.from_iterable(temp_landmark_list))

    # Normalization
    max_value = max(list(map(abs, temp_landmark_list)))

    def normalize_(n):
        return n / max_value

    temp_landmark_list = list(map(normalize_, temp_landmark_list))

    return temp_landmark_list


if __name__ == '__main__':
    main()
