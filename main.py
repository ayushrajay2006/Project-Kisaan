# main.py
# This is the main entry point for our AI Farmer Assistant application.

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Import the function from our new orchestrator file
from orchestrator import listen_and_transcribe

# --- Pre-flight Check for Microphone ---
# This is an important check. The speech_recognition library requires PyAudio,
# which in turn requires a system library called PortAudio.
# If PortAudio is not installed, the app will crash on startup.
try:
    import speech_recognition as sr
    # Check for microphone availability
    sr.Microphone()
except ImportError:
    print("PyAudio is not installed. Please install it with 'pip install PyAudio'")
except OSError:
    print("\n--- MICROPHONE NOT FOUND ---")
    print("This application requires a microphone.")
    print("Please ensure a microphone is connected and configured.")
    print("On Linux, you may need to install 'portaudio19-dev' (sudo apt-get install portaudio19-dev)")
    print("On macOS, you may need to install 'portaudio' (brew install portaudio)\n")
# --- End of Pre-flight Check ---


app = FastAPI(
    title="AI Farmer Assistant API",
    description="An AI-powered assistant to help farmers with pricing, crop diseases, and government schemes.",
    version="0.1.0",
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


# We use a POST request here because this operation causes an action to happen on the server.
@app.post("/listen")
def handle_listen(request: ListenRequest):
    """
    Listens to the microphone, transcribes the speech, and returns the text.
    
    This endpoint simulates a farmer speaking to the assistant.
    """
    print(f"Received request to listen in language: {request.language_code}")
    result = listen_and_transcribe(language_code=request.language_code)
    
    if result["status"] == "error":
        # If something went wrong, we return an HTTP error with the message.
        raise HTTPException(status_code=400, detail=result["message"])
        
    return result

# To run this application:
# 1. Make sure your virtual environment is activated.
# 2. In your terminal, run: uvicorn main:app --reload
# 3. Open your browser to http://127.0.0.1:8000/docs