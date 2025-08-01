# main.py
# This is the main entry point for our AI Farmer Assistant application.
# It now integrates the intent recognition logic.

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Import both functions from our orchestrator file
from orchestrator import listen_and_transcribe, recognize_intent

# --- Pre-flight Check for Microphone (Unchanged) ---
try:
    import speech_recognition as sr
    sr.Microphone()
except ImportError:
    print("PyAudio is not installed. Please install it with 'pip install PyAudio'")
except OSError:
    print("\n--- MICROPHONE NOT FOUND ---\nThis application requires a microphone.\nPlease ensure a microphone is connected and configured.\n")
# --- End of Pre-flight Check ---


app = FastAPI(
    title="AI Farmer Assistant API",
    description="An AI-powered assistant to help farmers with pricing, crop diseases, and government schemes.",
    version="0.2.1", # Version bump for the bug fix!
)

# Pydantic model for language selection
class ListenRequest(BaseModel):
    language_code: str = "en-IN" # e.g., "en-IN", "hi-IN", "te-IN", "ta-IN"

@app.get("/")
def read_root():
    """
    Root endpoint to check if the server is running.
    """
    return {"message": "Welcome to the AI Farmer Assistant! The server is running."}


@app.post("/listen_and_understand")
def handle_listen_and_understand(request: ListenRequest):
    """
    Listens, transcribes, and understands the user's intent.
    
    This endpoint now performs the full orchestrator workflow.
    """
    print(f"Received request to listen in language: {request.language_code}")
    
    # Step 1: Listen and Transcribe
    transcription_result = listen_and_transcribe(language_code=request.language_code)
    
    if transcription_result["status"] == "error":
        raise HTTPException(status_code=400, detail=transcription_result["message"])
    
    # --- BUG FIX ---
    # Correctly extract the transcribed text and language from the result dictionary.
    transcribed_text = transcription_result["transcription"]
    language_code = transcription_result["language"]
    
    # Step 2: Recognize Intent
    intent = recognize_intent(transcribed_text, language_code)
    
    # Step 3: Return the full analysis
    return {
        "status": "success",
        "transcription": transcribed_text, # This will now contain the correct text
        "language": language_code,
        "intent": intent
    }

# To run this application:
# 1. Make sure your virtual environment is activated.
# 2. In your terminal, run: uvicorn main:app --reload
# 3. Open your browser to http://127.0.0.1:8000/docs