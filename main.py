# main.py
# The server now delegates to the Market Guru agent when appropriate.

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Import functions from our agents
from orchestrator import listen_and_transcribe, recognize_intent
from market_guru import get_market_price # <-- New Import

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
    version="0.3.0", # Version bump for new feature!
)

class ListenRequest(BaseModel):
    language_code: str = "en-IN"

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Farmer Assistant! The server is running."}


@app.post("/listen_and_understand")
def handle_listen_and_understand(request: ListenRequest):
    """
    Listens, transcribes, understands intent, and delegates to the correct agent.
    """
    print(f"Received request to listen in language: {request.language_code}")
    
    # Step 1: Listen and Transcribe
    transcription_result = listen_and_transcribe(language_code=request.language_code)
    if transcription_result["status"] == "error":
        raise HTTPException(status_code=400, detail=transcription_result["message"])
    
    transcribed_text = transcription_result["transcription"]
    language_code = transcription_result["language"]
    
    # Step 2: Recognize Intent
    intent = recognize_intent(transcribed_text, language_code)
    
    # --- Step 3: Delegate to Specialist Agent ---
    agent_response = None
    if intent == "Market_Analysis":
        # If the intent is to get a price, call the Market Guru
        agent_response = get_market_price(transcribed_text)
    elif intent == "Crop_Health_Diagnosis":
        # Placeholder for the next agent we will build
        agent_response = {"status": "info", "message": "Crop health agent is not yet implemented."}
    elif intent == "Scheme_Information":
        # Placeholder
        agent_response = {"status": "info", "message": "Scheme information agent is not yet implemented."}
    elif intent == "Weather_Forecast":
        # Placeholder
        agent_response = {"status": "info", "message": "Weather forecast agent is not yet implemented."}


    # Step 4: Return the final, combined analysis
    return {
        "status": "success",
        "transcription": transcribed_text,
        "language": language_code,
        "intent": intent,
        "agent_response": agent_response # The response from the specialist agent
    }