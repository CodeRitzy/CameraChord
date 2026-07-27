import math
import cv2

def get_segment_from_point(
        point_x: int,
        point_y: int,
        center_x: int,
        center_y: int,
        inner_radius: int,
        outer_radius: int,
        segment_count: int,

) -> int | None:
    dx = point_x - center_x
    dy = point_y - center_y
    distance = (dx**2 + dy**2) ** 0.5

    # if distance is near center or too far from wheel
    if distance < inner_radius or distance > outer_radius:
        return None
    
    # angle calculation 
    angle = math.degrees(math.atan2(dy, dx))
    angle = (angle + 360) % 360
    
    segment_size = 360 / segment_count
    return int(angle // segment_size)


def draw_chord_wheel(
    frame,
    center_x: int,
    center_y: int,
    inner_radius: int,
    outer_radius: int,
    chords: list[str],
    selected_segment: int | None,
) -> None:
    segment_count = len(chords)
    segment_size = 360 / segment_count

    cv2.circle(frame, (center_x, center_y), outer_radius, (255, 255, 255), 2)
    cv2.circle(frame, (center_x, center_y), inner_radius, (255, 255, 255), 2)

    for index, chord in enumerate(chords):
        angle_degrees = index * segment_size
        angle_radians = math.radians(angle_degrees)

        line_end_x = int(center_x + outer_radius * math.cos(angle_radians))
        line_end_y = int(center_y + outer_radius * math.sin(angle_radians))

        if index == selected_segment:
            color = (0, 255, 0)
            thickness = 3
        else:
            color = (255, 255, 255)
            thickness = 2

        cv2.line(
            frame,
            (center_x, center_y),
            (line_end_x, line_end_y),
            color,
            thickness,
        )

        label_angle = math.radians(angle_degrees + segment_size / 2)
        label_radius = (inner_radius + outer_radius) // 2
        label_x = int(
            center_x + label_radius * math.cos(label_angle)
        )
        label_y = int(
            center_y + label_radius * math.sin(label_angle)
        )

        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.8
        text_thickness = 2

        text_size, _ = cv2.getTextSize(
            chord,
            font,
            font_scale,
            text_thickness,
        )

        text_width, text_height = text_size

        text_x = label_x - text_width // 2
        text_y = label_y + text_height // 2

        # Dark outline keeps the chord readable over the camera.
        cv2.putText(
            frame,
            chord,
            (text_x, text_y),
            font,
            font_scale,
            (0, 0, 0),
            5,
        )

        cv2.putText(
            frame,
            chord,
            (text_x, text_y),
            font,
            font_scale,
            color,
            text_thickness,
        )
    if selected_segment is not None:
        selected_chord = chords[selected_segment]

        center_font = cv2.FONT_HERSHEY_SIMPLEX
        center_scale = 1.6
        center_thickness = 3

        center_size, _ = cv2.getTextSize(
            selected_chord,
            center_font,
            center_scale,
            center_thickness,
        )

        center_text_width, center_text_height = center_size

        center_text_x = center_x - center_text_width // 2
        center_text_y = center_y + center_text_height // 2

        cv2.putText(
            frame,
            selected_chord,
            (center_text_x, center_text_y),
            center_font,
            center_scale,
            (0, 0, 0),
            7,
        )

        cv2.putText(
            frame,
            selected_chord,
            (center_text_x, center_text_y),
            center_font,
            center_scale,
            (0, 255, 0),
            center_thickness,
        )


        

        