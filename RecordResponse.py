import pyaudio
import wave
import io
import struct
import time
import math

# Constants
RATE = 16000
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
Threshold = 10
TIMEOUT_LENGTH = 2.3
SHORT_NORMALIZE = (1.0 / 32768.0)
swidth = 2


class Recorder:

    @staticmethod
    def rms(frame):
        count = len(frame) // swidth
        format = "%dh" % count
        shorts = struct.unpack(format, frame)

        sum_squares = 0.0
        for sample in shorts:
            n = sample * SHORT_NORMALIZE
            sum_squares += n * n
        rms = math.pow(sum_squares / count, 0.5)

        return rms * 1000

    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=FORMAT,
                                  channels=CHANNELS,
                                  rate=RATE,
                                  input=True,
                                  frames_per_buffer=CHUNK)

    def record(self):
        print('Noise detected, recording beginning')
        rec = []
        silent_chunks = 0
        max_silent_chunks = int(TIMEOUT_LENGTH * RATE / CHUNK)

        while True:
            data = self.stream.read(CHUNK)
            rec.append(data)

            if self.rms(data) < Threshold:
                silent_chunks += 1
            else:
                silent_chunks = 0

            if silent_chunks > max_silent_chunks:
                print("Silence detected, stopping recording.")
                break

        return b''.join(rec)

    def listen(self):
        print('Listening beginning')
        while True:
            input_data = self.stream.read(CHUNK)
            if self.rms(input_data) > Threshold:
                audio_data = self.record()
                return audio_data


def record_audio():
    recorder = Recorder()
    audio_data = recorder.listen()

    audio_buffer = io.BytesIO()
    with wave.open(audio_buffer, 'wb') as wave_file:
        wave_file.setnchannels(CHANNELS)
        wave_file.setsampwidth(recorder.p.get_sample_size(FORMAT))
        wave_file.setframerate(RATE)
        wave_file.writeframes(audio_data)

    audio_buffer.seek(0)
    return audio_buffer
