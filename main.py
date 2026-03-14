import os
import json
from dotenv import load_dotenv
from router import route_and_respond

# Load API Key from .env file
load_dotenv()
key = os.getenv("GROQ_API_KEY")
if key:
    print(f"✅ API Key found: {key[:7]}...") # Shows only the first few characters for safety
else:
    print("❌ API Key NOT found! Check your .env file.")

def run_test_suite():
    test_messages = [
        "how do i sort a list of objects in python?",
        "explain this sql query for me",
        "This paragraph sounds awkward, can you help me fix it?",
        "I'm preparing for a job interview, any tips?",
        "what's the average of these numbers: 12, 45, 23, 67, 34",
        "Help me make this better.",
        "I need to write a function that takes a user id and returns their profile, but also i need help with my resume.",
        "hey",
        "Can you write me a poem about clouds?",
        "Rewrite this sentence to be more professional.",
        "I'm not sure what to do with my career.",
        "what is a pivot table",
        "fxi thsi bug pls: for i in range(10) print(i)",
        "How do I structure a cover letter?",
        "My boss says my writing is too verbose."
    ]

    print(f"🚀 Starting Router Test Suite ({len(test_messages)} messages)...\n")
    print("-" * 50)

    for i, message in enumerate(test_messages, 1):
        print(f"Test {i}: '{message}'")
        try:
            response = route_and_respond(message)
            print(f"Response: {response[:100]}...") # Print preview of response
        except Exception as e:
            print(f"Error processing test {i}: {e}")
        print("-" * 50)

    print("\n✅ All tests complete. Check 'route_log.jsonl' for details.")

if __name__ == "__main__":
    if not os.getenv("GROQ_API_KEY"):
        print("❌ Error: GROQ_API_KEY not found in environment.")
    else:
        run_test_suite()