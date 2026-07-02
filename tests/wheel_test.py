from camerachord.wheel import get_segment_from_point

def test_point_below_center_is_segment_one_for_seven_segments():
    segment = get_segment_from_point(
        point_x=100,
        point_y=150,
        center_x=100,
        center_y=100,
        inner_radius=20,
        outer_radius=100,
        segment_count=7,
    )

    assert segment == 1


def test_point_above_center_is_segment_five_for_seven_segments():
    segment = get_segment_from_point(
        point_x=100,
        point_y=50,
        center_x=100,
        center_y=100,
        inner_radius=20,
        outer_radius=100,
        segment_count=7,
    )

    assert segment == 5