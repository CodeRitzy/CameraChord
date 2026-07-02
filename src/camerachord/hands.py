import cv2
import mediapipe as mp


class HandTracker:
    def __init__(self, model_path: str = "assets/models/hand_landmarker.task") -> None:
        base_options = mp.tasks.BaseOptions(model_asset_path=model_path)

        options = mp.tasks.vision.HandLandmarkerOptions(
            base_options = base_options,
            running_mode = mp.tasks.vision.RunningMode.VIDEO,
            num_hands = 1,
            min_hand_detection_confidence = 0.7,
            min_tracking_confidence = 0.7,
        )

        self._landmarker = mp.tasks.vision.HandLandmarker.create_from_options(options)
        self._timestamp_ms = 0

    def find_index_fingertip(self, frame) -> tuple[int, int] | None:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        self._timestamp_ms += 33
        result = self._landmarker.detect_for_video(mp_image, self._timestamp_ms)

        if not result.hand_landmarks:
            return None
        
        index_tip = result.hand_landmarks[0][8]

        height, width, _ = frame.shape

        x = int(index_tip.x * width)
        y = int(index_tip.y * height)

        return x, y
    
    def close(self) -> None:
        self._landmarker.close()

        