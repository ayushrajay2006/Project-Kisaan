# main.py
# The server now has a dedicated endpoint for disease diagnosis via image upload.

from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel

# Import functions from our agents
from orchestrator import listen_and_transcribe, recognize_intent
from market_guru import get_market_price
from digital_pathologist import diagnose_crop_health # <-- New Import

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
    version="0.4.0", # Version bump for new agent!
)

class ListenRequest(BaseModel):
    language_code: str = "en-IN"

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Farmer Assistant! The server is running."}


@app.post("/listen_and_understand")
def handle_listen_and_understand(request: ListenRequest):
    """
    Handles the voice-based interaction workflow.
    """
    # (This function is unchanged from the previous step)
    print(f"Received request to listen in language: {request.language_code}")
    
    transcription_result = listen_and_transcribe(language_code=request.language_code)
    if transcription_result["status"] == "error":
        raise HTTPException(status_code=400, detail=transcription_result["message"])
    
    transcribed_text = transcription_result["transcription"]
    language_code = transcription_result["language"]
    intent = recognize_intent(transcribed_text, language_code)
    
    agent_response = None
    if intent == "Market_Analysis":
        agent_response = get_market_price(transcribed_text)
    # The other intents still return placeholder messages
    else:
        agent_response = {"status": "info", "message": f"Agent for intent '{intent}' is not yet fully implemented for voice commands."}

    return {
        "status": "success",
        "transcription": transcribed_text,
        "language": language_code,
        "intent": intent,
        "agent_response": agent_response
    }


# --- NEW ENDPOINT FOR IMAGE UPLOADS ---
@app.post("/diagnose_disease")
async def handle_diagnose_disease(image: UploadFile = File(...)):
    """
    Accepts an image upload and passes it to the Digital Pathologist agent.
    
    To use this, you need to send a POST request with 'multipart/form-data'.
    The interactive docs at /docs handle this for you automatically.
    """
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File uploaded is not an image.")
        
    # Call the specialist agent with the file details
    diagnosis_result = diagnose_crop_health(
        image_file_name=image.filename,
        image_content_type=image.content_type
    )
    
    return diagnosis_result