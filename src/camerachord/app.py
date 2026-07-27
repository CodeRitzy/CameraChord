import cv2

from camerachord.audio import ChordPlayer
from camerachord.camera import open_camera
from camerachord.hands import HandTracker
from camerachord.music import (
    Mode,
    Root,
    get_chords_in_key,
    get_triads_in_key,
)
from camerachord.ui import Dropdown
from camerachord.wheel import draw_chord_wheel, get_segment_from_point
from collections import Counter, deque


def main() -> None:
    tracker = HandTracker()
    camera = open_camera()
    player = ChordPlayer()

    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1600)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 900)

    root_options = list(Root)
    mode_options = list(Mode)

    root_dropdown = Dropdown(
        x=20,
        y=70,
        width=130,
        height=40,
        options=[root.display_name for root in root_options],
        selected_index=2,
    )

    mode_dropdown = Dropdown(
        x=170,
        y=70,
        width=140,
        height=40,
        options=[mode.display_name for mode in mode_options],
        selected_index=0,
    )

    selected_root = root_options[root_dropdown.selected_index]
    selected_mode = mode_options[mode_dropdown.selected_index]

    chords = get_chords_in_key(selected_root, selected_mode)
    triads = get_triads_in_key(selected_root, selected_mode)

    window_name = "CameraChord"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 1600, 900)

    def handle_mouse(event, x, y, flags, parameter):
        if event == cv2.EVENT_LBUTTONDOWN:
            root_dropdown.handle_click(x, y)
            mode_dropdown.handle_click(x, y)

    cv2.setMouseCallback(window_name, handle_mouse)

    segment_history = deque([None] * 5, maxlen=5)

    try:
        while True:
            new_root = root_options[root_dropdown.selected_index]
            new_mode = mode_options[mode_dropdown.selected_index]

            if new_root != selected_root or new_mode != selected_mode:
                player.stop()

                selected_root = new_root
                selected_mode = new_mode

                chords = get_chords_in_key(
                    selected_root,
                    selected_mode,
                )
                triads = get_triads_in_key(
                    selected_root,
                    selected_mode,
                )

            success, frame = camera.read()

            if not success:
                raise RuntimeError("Could not read frame from webcam")

            frame = cv2.flip(frame, 1)

            height, width, _ = frame.shape

            center_x = width // 2
            center_y = height // 2
            outer_radius = min(width, height) // 3
            inner_radius = outer_radius // 3

            index_tip = tracker.find_index_fingertip(frame)
            detected_segment = None

            if index_tip is not None:
                point_x, point_y = index_tip

                detected_segment = get_segment_from_point(
                    point_x,
                    point_y,
                    center_x,
                    center_y,
                    inner_radius,
                    outer_radius,
                    len(chords),
                )

                cv2.circle(
                    frame,
                    index_tip,
                    8,
                    (0, 255, 0),
                    -1,
                )

            segment_history.append(detected_segment)

            selected_segment = Counter(
                segment_history
            ).most_common(1)[0][0]

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
                f"Key: {selected_root.display_name} "
                f"{selected_mode.display_name}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2,
            )

            root_dropdown.draw(frame, "Root")
            mode_dropdown.draw(frame, "Mode")

            cv2.imshow(window_name, frame)

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