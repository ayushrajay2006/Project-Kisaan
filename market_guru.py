# market_guru.py
# This is our first specialist agent. Its job is to find market prices for crops.

import logging

# In a real application, this data would come from a database or a live API call.
# For now, we use a simple dictionary to simulate a database.
MOCK_PRICE_DATABASE = {
    "tomato": {"price": 2100, "unit": "quintal", "market": "Rythu Bazar, Mehdipatnam"},
    "cotton": {"price": 7500, "unit": "quintal", "market": "Adilabad Market Yard"},
    "chilli": {"price": 15000, "unit": "quintal", "market": "Guntur Mirchi Yard"},
    "turmeric": {"price": 8200, "unit": "quintal", "market": "Nizamabad Market"},
    # --- Mapped to Telugu ---
    "టమోటా": {"price": 2100, "unit": "quintal", "market": "రైతు బజార్, మెహదీపట్నం"},
    "పత్తి": {"price": 7500, "unit": "quintal", "market": "ఆదిలాబాద్ మార్కెట్ యార్డ్"},
}


def get_market_price(text):
    """
    Analyzes the text to find a crop and returns its market price.

    Args:
        text (str): The transcribed text from the user.

    Returns:
        dict: A dictionary containing the price details, or an error message.
    """
    text_lower = text.lower()
    
    # Simple entity extraction: find which crop the user is asking about.
    for crop in MOCK_PRICE_DATABASE.keys():
        if crop in text_lower:
            logging.info(f"Market Guru found crop: {crop}")
            price_info = MOCK_PRICE_DATABASE[crop]
            # Add the crop name to the response for clarity
            price_info["crop"] = crop 
            return {
                "status": "success",
                "data": price_info
            }
            
    logging.warning(f"Market Guru could not find a known crop in text: '{text}'")
    return {
        "status": "error",
        "message": "Sorry, I could not identify the crop you are asking about. Please try again."
    }