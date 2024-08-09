import streamlit as st
from AskQuestion import ask_question, play_audio
from RecordResponse import record_audio
from ResponseTranscription import transcribe_audio
from Scoring import score
import UpdateSheet
import os


def main():
    st.title("Interview Process")

    if 'num_questions' not in st.session_state:
        st.session_state.num_questions = 0
        st.session_state.total_score = 0
        st.session_state.average_score = 0
        st.session_state.responses = []
        st.session_state.interview_started = False
        st.session_state.greeting_played = False
        st.session_state.current_question_text = ""
        st.session_state.recording_in_progress = False

    if not st.session_state.interview_started:
        if st.button("Start Interview"):
            st.session_state.interview_started = True
            st.session_state.greeting_played = True
            st.session_state.current_question_text = "Hello, I will be interviewing you now. Please state your name."
            st.write(st.session_state.current_question_text)
            play_audio(st.session_state.current_question_text)
            st.session_state.recording_in_progress = True
            st.experimental_rerun()

    if st.session_state.recording_in_progress:
        st.write("Speak Now")
        audio_buffer = record_audio()
        with open("temp_audio.wav", "wb") as f:
            f.write(audio_buffer.getvalue())
        candidate_response = transcribe_audio("temp_audio.wav")
        st.session_state.responses.append(candidate_response)
        st.write(f"Candidate Response: {candidate_response}")
        st.session_state.recording_in_progress = False
        st.experimental_rerun()

    if st.session_state.interview_started and not st.session_state.recording_in_progress:
        if st.session_state.num_questions == 0:
            if st.button("Next Question"):
                question = ask_question()
                st.session_state.current_question_text = question
                st.write(question)
                play_audio(question)
                st.session_state.recording_in_progress = True
                st.session_state.num_questions += 1
                st.experimental_rerun()
        else:
            st.write(st.session_state.current_question_text)
            if st.button("Next Question"):
                question = ask_question()
                st.session_state.current_question_text = question
                st.write(question)
                play_audio(question)
                st.session_state.recording_in_progress = True
                st.experimental_rerun()
            else:
                st.write("Speak Now")
                audio_buffer = record_audio()
                with open("temp_audio.wav", "wb") as f:
                    f.write(audio_buffer.getvalue())
                candidate_response = transcribe_audio("temp_audio.wav")
                st.session_state.responses.append(candidate_response)
                st.write(f"Candidate Response: {candidate_response}")

                # Score the response
                response_score = score(
                    st.session_state.current_question_text, candidate_response)
                st.session_state.total_score += response_score
                st.write(f"Score for the response: {response_score}")
                st.session_state.num_questions += 1
                st.experimental_rerun()

    if st.session_state.interview_started and st.button("End Interview"):
        if st.session_state.num_questions > 0:
            st.session_state.average_score = st.session_state.total_score / \
                st.session_state.num_questions
            UpdateSheet.main(st.session_state.average_score)
            st.write(f"Average Score: {st.session_state.average_score}")
        else:
            st.write("No questions were asked.")

        # Mimic keyboard interrupt for script termination
        st.write("Interview ended. Closing the application...")
        st.stop()
        os._exit(0)


if __name__ == "__main__":
    main()
