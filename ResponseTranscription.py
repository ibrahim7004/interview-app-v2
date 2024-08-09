import assemblyai as aai

# Set AssemblyAI API key
aai.settings.api_key = "bbd6c60f718a419d99fa7e70b45fa7db"


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
