import cv2

def open_camera(camera_index: int = 0) -> cv2.VideoCapture:
    camera = cv2.VideoCapture(camera_index)

    if not camera.isOpened():
        raise RuntimeError("Webcam cannot be opened")
    
    return camera