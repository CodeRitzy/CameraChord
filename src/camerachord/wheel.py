import math

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