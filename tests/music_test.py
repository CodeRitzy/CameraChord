from camerachord.music import Root, Mode, build_scale, get_chords_in_key

def test_build_d_major_scale():
    scale = build_scale(Root.D, Mode.MAJOR)

    assert [note.display_name for note in scale] == [
        "D",
        "E",
        "F#",
        "G",
        "A",
        "B",
        "C#",
    ]


def test_build_a_minor_scale():
    scale = build_scale(Root.A, Mode.MINOR)

    assert [note.display_name for note in scale] == [
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
    ]


def test_get_chords_in_d_major():
    chords = get_chords_in_key(Root.D, Mode.MAJOR)

    assert chords == [
        "D",
        "Em",
        "F#m",
        "G",
        "A",
        "Bm",
        "C#dim",
    ]


def test_get_chords_in_a_minor():
    chords = get_chords_in_key(Root.A, Mode.MINOR)

    assert chords == [
        "Am",
        "Bdim",
        "C",
        "Dm",
        "Em",
        "F",
        "G",
    ]