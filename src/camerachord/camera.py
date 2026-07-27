import math

import cv2


def open_camera(camera_index: int = 0) -> cv2.VideoCapture:
    camera = cv2.VideoCapture(camera_index)

    if not camera.isOpened():
        raise RuntimeError("Could not open webcam")

    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1600)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 900)

    return camera
