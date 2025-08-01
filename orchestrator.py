# orchestrator.py
# This file will contain the logic for our main Orchestrator Agent.
# Its primary job is to listen to the user and delegate tasks.

import speech_recognition as sr
import logging

# Configure logging to see informational messages
logging.basicConfig(level=logging.INFO)

def listen_and_transcribe(language_code="en-IN"):
    """
    Listens for audio input from the microphone and transcribes it into text
    using Google's Web Speech API.

    Args:
        language_code (str): The language code for transcription (e.g., "en-IN", "hi-IN", "te-IN").

    Returns:
        dict: A dictionary containing the status and the transcribed text or an error message.
    """
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        # Adjust for ambient noise to improve accuracy.
        # This listens for 1 second to calibrate the energy threshold.
        logging.info("Calibrating for ambient noise... Please be quiet.")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        logging.info(f"Listening in {language_code}...")
        print("Say something!")

        try:
            # Listen for the first phrase and extract it into audio data
            audio_data = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            logging.info("Recognizing...")

            # Recognize speech using Google Web Speech API
            # This is a free and convenient API built into the library for testing.
            # For the final product, we will switch to the more robust Google Cloud Speech-to-Text API.
            text = recognizer.recognize_google(audio_data, language=language_code)
            
            logging.info(f"Transcription: {text}")
            return {"status": "success", "transcription": text, "language": language_code}

        except sr.WaitTimeoutError:
            error_message = "No speech detected within the timeout period."
            logging.error(error_message)
            return {"status": "error", "message": error_message}
        
        except sr.UnknownValueError:
            error_message = "Google Web Speech API could not understand the audio."
            logging.error(error_message)
            return {"status": "error", "message": error_message}

        except sr.RequestError as e:
            error_message = f"Could not request results from Google Web Speech API; {e}"
            logging.error(error_message)
            return {"status": "error", "message": error_message}
        
        except Exception as e:
            error_message = f"An unexpected error occurred: {e}"
            logging.error(error_message)
            return {"status": "error", "message": error_message}