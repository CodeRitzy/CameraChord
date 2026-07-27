import cv2

from camerachord.audio import ChordPlayer
from camerachord.camera import open_camera
from camerachord.hands import HandTracker
from camerachord.music import Mode, Root, get_chords_in_key, get_triads_in_key
from camerachord.wheel import draw_chord_wheel, get_segment_from_point

def main() -> None:
    tracker = HandTracker()
    camera = open_camera()
    player = ChordPlayer()

    selected_root = Root.D
    selected_mode = Mode.MAJOR
    chords = get_chords_in_key(selected_root, selected_mode)
    triads = get_triads_in_key(selected_root, selected_mode)

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
            max_wheel_radius = min(width, height) // 3
            
            outer_radius = max_wheel_radius
            inner_radius = outer_radius // 3
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

                cv2.circle(frame, index_tip, 8, (0, 255, 0), -1)

            if selected_segment is not None:
                selected_chord = chords[selected_segment]
            else:
                selected_chord = None

            if selected_segment is not None:
                player.play_chord(triads[selected_segment])
            else:
                player.stop()

            draw_chord_wheel(
                frame,
                center_x,
                center_y,
                inner_radius,
                outer_radius,
                chords,
                selected_segment,
            )
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
        player.close()
        tracker.close()
        camera.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
