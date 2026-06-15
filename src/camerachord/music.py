from enum import Enum

CHROMATIC_NOTE_COUNT = 12
class Root(Enum):
    C = (0, "C")
    C_SHARP = (1, "C#")
    D = (2, "D")
    D_SHARP = (3, "D#")
    E = (4, "E")
    F = (5, "F")
    F_SHARP = (6, "F#")
    G = (7, "G")
    G_SHARP = (8, "G#")
    A = (9, "A")
    A_SHARP = (10, "A#")
    B = (11, "B")

    @property
    def pitch(self):
        return self.value[0]
    
    @property
    def display_name(self):
        return self.value[1]

class Mode(Enum):
    MAJOR = "Major"
    MINOR = "Minor"

    @property
    def display_name(self):
        return self.value

MODE_INTERVALS = {
    Mode.MAJOR: [0, 2, 4, 5, 7, 9, 11],
    Mode.MINOR: [0, 2, 3, 5, 7, 8, 10]
}

class ChordType(Enum):
    MAJOR = ""
    MINOR = "m"
    DIMINISHED = "dim"

    @property
    def chordType(self):
        return self.value;

def get_root_options() -> list[Root]:
    return list(Root)
def get_mode_options() -> list[Mode]:
    return list(Mode)

def get_root_from_pitch(pitch: int):
    normal_pitch = pitch % 12
    for root in Root:
        if normal_pitch == root.pitch:
            return root
    raise ValueError(f"No root found for pitch: {pitch}")
    
def build_scale(root: Root, mode: Mode) -> list[Root]:
    scale = []
    for interval in MODE_INTERVALS[mode]:
        scale.append(get_root_from_pitch((root.pitch + interval) % 12))
    return scale

def build_triads(scale: list[Root]) -> list[tuple[Root, Root, Root]]:
    triads = []
    for degree in range(len(scale)):
        root = scale[degree]
        third = scale[(degree + 2) % len(scale)]
        fifth = scale[(degree + 4) % len(scale)]
        triads.append((root, third, fifth))
    return triads

def get_chord_type(root: Root, third: Root, fifth: Root) -> ChordType:
    third_interval = (third.pitch - root.pitch) % CHROMATIC_NOTE_COUNT
    fifth_interval = (fifth.pitch - root.pitch) % CHROMATIC_NOTE_COUNT
    
    if third_interval == 4 and fifth_interval == 7:
        return ChordType.MAJOR
    if third_interval == 3 and fifth_interval == 7:
        return ChordType.MINOR
    if third_interval == 3 and fifth_interval == 6:
        return ChordType.DIMINISHED
    
    raise ValueError("Unknown chord quality")

def get_chord_name(root: Root, third: Root, fifth: Root) -> str:
    return root.display_name + get_chord_type(root, third, fifth).chordType

def get_chords_in_key(root: Root, mode: Mode) -> list[str]:
    scale = build_scale(root, mode)
    triads = build_triads(scale)
    chords = []
    for triad in triads:
        chords.append(get_chord_name(triad[0], triad[1], triad[2]))
    return chords
