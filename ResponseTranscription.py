import assemblyai as aai
import os
from dotenv import load_dotenv

load_dotenv()
aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")


def transcribe_audio(audio_file_path):
    with open(audio_file_path, "rb") as audio_file:
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_file)
        return transcript.text


if __name__ == "__main__":
    import sys
    audio_file_path = sys.argv[1]
    transcription = transcribe_audio(audio_file_path)
    print(f"Transcription: {transcription}")
