import google.generativeai as genai
import os
import json

# Load environment variables
from dotenv import load_dotenv

load_dotenv()


class GeminiAPI:
    def __init__(self) -> None:
        # prepare the large language model
        GEMINI_API_KEY = os.environ.get("GOOGLE_CLOUD_API_KEY")

        # Initialize the Gemini API
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(
            "gemini-1.5-pro-latest",
            generation_config=genai.GenerationConfig(
                max_output_tokens=8000,
                temperature=2, # 1.0 is max for gemini 1.0, 2.0 is max for gemini 1.5
            ),
        )

        # configure constants, like the question format and the number of questions
        self.question_count = 10

        self.question_list_prompt = """

        [
            {
                "team": "UCI Anteaters",
                "questions": [
                    {
                        "question": "What is the mascot of UC Irvine?",
                        "answer_options": ["Anteater", "Aggie", "Triton", "Gaucho"]
                        "correct_indices": [0]
                    }
                ]
            }
        ]

        The team should match the inputted team name. The answer_options represent possible answer choices a contestant can choose from. The correct_indices represent the index of the correct answer in the answer_options list.

        """

    def generate_system_prompt(self, team1, context):

        return f"""
    You are a sports trivia host, specializing in College Sports trivia.

    You are known for creating engaging trivia questions, and you will be creating a list of questions.

    You will create a list of {self.question_count} questions about this team:

    {team1}

    Here is an article detailing information about the team that you can use to create your questions:

    {context}

    Output your question list in a valid JSON format.

    Here is an example output. If one of the teams was the UCI Anteaters, the output could look like this:

    {self.question_list_prompt}
    """

    def generate_embeddings_from_list(self, text_list: list):
        result = genai.embed_content(model="models/text-embedding-004", content=text_list, task_type="question_answering")
        for embedding in result['embedding']:
            print(str(embedding)[:50], '... TRIMMED]')
        return result


    def generate_embeddings(self, text: str, verbose: bool = False):
        result = genai.embed_content(model="models/text-embedding-004", content=text, task_type="retrieval_document")
        if verbose:
            # Print just a part of the embedding to keep the output manageable
            print(str(result['embedding'])[:50], '... TRIMMED]')
        return result
    
    # basic function to generate questions from a prompt and return text
    def generate(self, prompt: str):
        response = self.model.generate_content(prompt)
        return response.text

    # Generate the questions, and return as an array of questions
    def generate_and_format_questions(self, team, context):

        # generate the system prompt
        prompt = self.generate_system_prompt(team, context)
        # generate the questions
        print("Generating questions...")
        response = self.generate(prompt)
        # trim, format, and return the questions
        response = response.strip()
        response = response.replace("json", "")
        response = response.replace("`", "")
        # convert to JSON format
        response = json.loads(response)
        return response

    # use this function to save the questions somewhere
    def save_questions(self, questions, team):
        # send question results to backend database
        # FIXME: For now, we will save the questions to a JSON file
        with open(f"{team}_questions.json", "w") as f:
            json.dump(questions, f)