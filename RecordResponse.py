import sounddevice as sd
import numpy as np
import wave
import io
import struct
import time
import math

# Constants
RATE = 16000
CHUNK = 1024
FORMAT = np.int16
CHANNELS = 1
Threshold = 10
TIMEOUT_LENGTH = 2.3
SHORT_NORMALIZE = (1.0 / 32768.0)
swidth = 2


class Recorder:

    @staticmethod
    def rms(frame):
        count = len(frame)
        shorts = np.frombuffer(frame, dtype=np.int16)

        sum_squares = np.sum(shorts.astype(np.float32) ** 2)
        rms = math.sqrt(sum_squares / count)

        return rms * 1000

    def __init__(self):
        self.stream = sd.InputStream(samplerate=RATE,
                                     channels=CHANNELS,
                                     dtype=FORMAT,
                                     blocksize=CHUNK)

    def record(self):
        print('Noise detected, recording beginning')
        rec = []
        silent_chunks = 0
        max_silent_chunks = int(TIMEOUT_LENGTH * RATE / CHUNK)

        self.stream.start()
        while True:
            data, _ = self.stream.read(CHUNK)
            rec.append(data)

            if self.rms(data) < Threshold:
                silent_chunks += 1
            else:
                silent_chunks = 0

            if silent_chunks > max_silent_chunks:
                print("Silence detected, stopping recording.")
                break
        self.stream.stop()

        return b''.join(rec)

    def listen(self):
        print('Listening beginning')
        self.stream.start()
        while True:
            input_data, _ = self.stream.read(CHUNK)
            if self.rms(input_data) > Threshold:
                audio_data = self.record()
                return audio_data
        self.stream.stop()


def record_audio():
    recorder = Recorder()
    audio_data = recorder.listen()

    audio_buffer = io.BytesIO()
    with wave.open(audio_buffer, 'wb') as wave_file:
        wave_file.setnchannels(CHANNELS)
        wave_file.setsampwidth(swidth)
        wave_file.setframerate(RATE)
        wave_file.writeframes(audio_data)

    audio_buffer.seek(0)
    return audio_buffer
