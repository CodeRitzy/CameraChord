import cv2

from camerachord.hands import HandTracker
from camerachord.camera import open_camera
from camerachord.music import Mode, Root, get_chords_in_key
from camerachord.wheel import get_segment_from_point

def main() -> None:
    tracker = HandTracker()
    camera = open_camera()
    selected_root = Root.D
    selected_mode = Mode.MAJOR
    chords = get_chords_in_key(selected_root, selected_mode)

    print(f"Selected key: {selected_root.display_name} {selected_mode.display_name}")
    print(f"Chords: {chords}")

    try:
        while True:

            success, frame = camera.read()

            if not success:
                raise RuntimeError("Could not read frame from webcam")
            
            frame = cv2.flip(frame, 1)

            height, width, _ = frame.shape

            center_x = width // 2
            center_y = height // 2
            inner_radius = 80
            outer_radius = 220
            segment_count = len(chords)

            
            index_tip = tracker.find_index_fingertip(frame)
            
            selected_segment = None
            if index_tip is not None:
                point_x, point_y = index_tip

                selected_segment = get_segment_from_point(
                    point_x,
                    point_y,
                    center_x,
                    center_y,
                    inner_radius,
                    outer_radius,
                    segment_count,
                )

            if selected_segment is not None:
                selected_chord = chords[selected_segment]
            else:
                selected_chord = None
            cv2.putText(
                frame,
                f"Key: {selected_root.display_name} {selected_mode.display_name}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2,
            )

            if selected_chord is not None:
                cv2.putText(
                    frame,
                    f"Selected: {selected_chord}",
                    (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2,
                )

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