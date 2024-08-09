import pandas as pd
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
from io import BytesIO
import tempfile
import os

# Define file path
CSV_PATH = 'new_data2.csv'


def ask_question():
    df = pd.read_csv(CSV_PATH)
    chosen_question = df.sample(n=1).iloc[0]
    df.drop(chosen_question.name, inplace=True)
    df.to_csv(CSV_PATH, index=False)
    return chosen_question['Question']


def play_audio(text):
    tts = gTTS(text=text, lang='en')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
        tts.save(temp_file.name)
        temp_file_path = temp_file.name

    with open(temp_file_path, 'rb') as f:
        audio_data = f.read()
    audio_buffer = BytesIO(audio_data)
    audio = AudioSegment.from_file(audio_buffer, format="mp3")
    audio = audio.speedup(playback_speed=1.1)
    play(audio)

    # Ensure the temporary file is deleted after reading its contents
    os.remove(temp_file_path)


if __name__ == "__main__":
    question = ask_question()
    play_audio(question)
