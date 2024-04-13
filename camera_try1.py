import cv2
import matplotlib.pyplot as plt
import time


def video_info():
    # Loading classifiers
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # Input video stream
    cap = cv2.VideoCapture(0)
    # To use a video file as input
    # cap = cv2.VideoCapture('demo.mp4')

    while True:
        _, img = cap.read()
        # Conversion to greyscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Detecting faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        # Drawing the outline
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            center_x = (x + w - x) // 2 + x
            center_y = (y + h - y) // 2 + y
            cv2.circle(img, (center_x, center_y), 10, (0, 255, 255), 2)

        # Display effects
        cv2.imshow('img', img)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
    cap.release()


if __name__ == "__main__":
    video_info()
