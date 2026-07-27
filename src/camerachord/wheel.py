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

       