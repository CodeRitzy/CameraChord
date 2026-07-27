import numpy as np
import pygame

from camerachord.music import Root


NOTE_FREQUENCIES = {
    Root.C: 261.63,
    Root.C_SHARP: 277.18,
    Root.D: 293.66,
    Root.D_SHARP: 311.13,
    Root.E: 329.63,
    Root.F: 349.23,
    Root.F_SHARP: 369.99,
    Root.G: 392.00,
    Root.G_SHARP: 415.30,
    Root.A: 440.00,
    Root.A_SHARP: 466.16,
    Root.B: 493.88,
}


def low_pass_filter(wave: np.ndarray, cutoff: float, sample_rate: int) -> np.ndarray:
    filtered_wave = np.zeros_like(wave)

    time_step = 1 / sample_rate
    resistance_capacitance = 1 / (2 * np.pi * cutoff)
    filter_amount = time_step / (resistance_capacitance + time_step)

    for index in range(1, len(wave)):
        filtered_wave[index] = (
            filtered_wave[index - 1]
            + filter_amount * (wave[index] - filtered_wave[index - 1])
        )

    return filtered_wave


class ChordPlayer:
    def __init__(self) -> None:
        self.sample_rate = 44100

        pygame.mixer.init(
            frequency=self.sample_rate,
            size=-16,
            channels=2,
        )

        self.channel = pygame.mixer.Channel(0)
        self.channel.set_volume(0.18)
        self.current_triad = None
        self.sound_cache = {}

    def create_chord_sound(
        self,
        triad: tuple[Root, Root, Root],
    ) -> pygame.mixer.Sound:
        duration = 4
        sample_count = self.sample_rate * duration
        time = np.arange(sample_count) / self.sample_rate

        wave = np.zeros(sample_count)

        for note in triad:
            frequency = NOTE_FREQUENCIES[note]

            normal_sine = np.sin(2 * np.pi * frequency * time)
            sub_sine = np.sin(2 * np.pi * (frequency / 2) * time)

            saw_phase = frequency * time
            saw_wave = 2 * (saw_phase - np.floor(saw_phase + 0.5))

            wave += (
                normal_sine * 0.45
                + sub_sine * 0.45
                + saw_wave * 0.10
            )

        wave /= len(triad)
        wave = low_pass_filter(wave, cutoff=900, sample_rate=self.sample_rate)

        maximum = np.max(np.abs(wave))
        if maximum > 0:
            wave /= maximum

        wave *= 0.45

        integer_wave = (wave * 32767).astype(np.int16)
        stereo_wave = np.column_stack((integer_wave, integer_wave))
        stereo_wave = np.ascontiguousarray(stereo_wave)

        return pygame.sndarray.make_sound(stereo_wave)

    def play_chord(self, triad: tuple[Root, Root, Root]) -> None:
        if triad == self.current_triad:
            return

        self.stop()

        if triad not in self.sound_cache:
            self.sound_cache[triad] = self.create_chord_sound(triad)

        self.current_triad = triad
        self.channel.play(self.sound_cache[triad], loops=-1, fade_ms=100)

    def stop(self) -> None:
        if self.current_triad is None:
            return

        self.channel.fadeout(150)
        self.current_triad = None

    def close(self) -> None:
        self.stop()
        pygame.mixer.quit()