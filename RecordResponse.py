import speech_recognition as sr
import wave
import io
from pydub import AudioSegment
from pydub.playback import play

# Constants
RATE = 16000
CHANNELS = 1
swidth = 2


class Recorder:

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone(sample_rate=RATE, chunk_size=1024)

    def record(self):
        print('Listening...')
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
            print("Recording complete.")
        return audio.get_wav_data()


def record_audio():
    recorder = Recorder()
    audio_data = recorder.record()

    audio_buffer = io.BytesIO(audio_data)
    with wave.open(audio_buffer, 'wb') as wave_file:
        wave_file.setnchannels(CHANNELS)
        wave_file.setsampwidth(swidth)
        wave_file.setframerate(RATE)
        wave_file.writeframes(audio_data)

    audio_buffer.seek(0)
    return audio_buffer


def play_audio(audio_buffer):
    audio_buffer.seek(0)
    audio_segment = AudioSegment.from_wav(audio_buffer)
    play(audio_segment)


# Example usage
if __name__ == "__main__":
    audio_buffer = record_audio()
    play_audio(audio_buffer)
