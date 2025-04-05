import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, value=600)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, value=600)
mp_draw = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hand = mp_hands.Hands(max_num_hands=1)

if not cam.isOpened():
    print("Stream Not Working")
    exit()

while True:
    ret, frame = cam.read() # The frame captured is in BGR
    if not ret:
        print("Stream Ended")
        break

    RGB_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR frame to RGB for MediaPipe processing
    result = hand.process(frame)
    if result.multi_hand_landmarks: # Iterating through positions
        for i in result.multi_hand_landmarks:
            handLandmarks = result.multi_hand_landmarks[0]
            mp_draw.draw_landmarks(frame, i, mp_hands.HAND_CONNECTIONS) # Drawing Hand Connections
            print(i)

    cv2.imshow("Camfeed", frame)

    if cv2.waitKey(1) == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()