import json
import os
from groq import Groq
from dotenv import load_dotenv # Add this import
from prompts import EXPERT_PROMPTS, CLASSIFIER_PROMPT

# Load variables here to ensure they are available for the client
load_dotenv() 

# Initialize client after loading env
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def classify_intent(message: str):
    try:
        # Groq is exceptionally fast for this lightweight task
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile", 
            messages=[
                {"role": "system", "content": CLASSIFIER_PROMPT},
                {"role": "user", "content": message}
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception:
        # Default to unclear if JSON parsing or API fails
        return {"intent": "unclear", "confidence": 0.0}

def route_and_respond(user_message: str):
    classification = classify_intent(user_message)
    intent = classification.get("intent", "unclear")
    confidence = classification.get("confidence", 0.0)

    # Thresholding logic
    if intent == "unclear" or confidence < 0.7:
        final_response = (
            "I'm not quite sure how to help with that. Are you looking for help "
            "with coding, data analysis, writing, or career advice?"
        )
    else:
        system_prompt = EXPERT_PROMPTS.get(intent)
        
        # Second call to the expert persona
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )
        final_response = response.choices[0].message.content

    log_request(intent, confidence, user_message, final_response)
    return final_response

def log_request(intent, confidence, message, response):
    log_entry = {
        "intent": intent,
        "confidence": confidence,
        "user_message": message,
        "final_response": response
    }
    with open("route_log.jsonl", "a") as f:
        f.write(json.dumps(log_entry) + "\n")