import cv2

from camerachord.hands import HandTracker
from camerachord.camera import open_camera

def main() -> None:
    tracker = HandTracker()
    camera = open_camera()

    try:
        while True:
            success, frame = camera.read()

            if not success:
                raise RuntimeError("Could not read frame from webcam")
            
            frame = cv2.flip(frame, 1)

            index_tip = tracker.find_index_fingertip(frame)

            if index_tip is not None:
                cv2.circle(frame, index_tip, 8, (0, 255, 0), -1)
            
            cv2.imshow("CameraChord", frame)

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break

    finally:
        tracker.close()
        camera.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()