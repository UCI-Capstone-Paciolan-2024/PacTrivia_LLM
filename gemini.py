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
def generate_and_format_questions(team):
    # geenrate the system prompt
    prompt = generate_system_prompt(team)
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

def generate_embeddings_from_list(text_list: list):
    result = genai.embed_content(model="models/text-embedding-004", content=text_list, task_type="question_answering")
    for embedding in result['embedding']:
        print(str(embedding)[:50], '... TRIMMED]')
    return result

def generate_embeddings(text: str):
    result = genai.embed_content(model="models/text-embedding-004", content=text, task_type="retrieval_document")
    # Print just a part of the embedding to keep the output manageable
    print(str(result['embedding'])[:50], '... TRIMMED]')
    return result

if __name__ == "__main__":
    response = generate_and_format_questions("UCI Anteaters")