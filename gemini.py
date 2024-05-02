import google.generativeai as genai
import os
from constants import generate_system_prompt
import json

# Load environment variables
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.environ.get("GOOGLE_CLOUD_API_KEY")

# Initialize the Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
    "gemini-1.5-pro-latest",
    generation_config=genai.GenerationConfig(
        max_output_tokens=8000,
        temperature=0,
    ),
)

def generate(prompt: str):
    response = model.generate_content(prompt)
    return response.text

# Generate the questions, and return as an array of questions
def generate_and_format_questions(team1, team2):
    # geenrate the system prompt
    prompt = generate_system_prompt(team1, team2)
    # generate the questions
    print("Generating questions...")
    response = generate(prompt)
    # trim, format, and return the questions
    response = response.strip()
    response = response.replace("json", "")
    response = response.replace("`", "")
    print(response)
    # convert to JSON format
    response = json.loads(response)
    return response

if __name__ == "__main__":
    response = generate_and_format_questions("UCI Anteaters", "UC Davis Aggies")