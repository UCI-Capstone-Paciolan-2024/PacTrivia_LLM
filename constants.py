question_count = 10

question_list_prompt = """

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
"""

def generate_system_prompt(team1):

    return f"""
You are a sports trivia host, specializing in College Sports trivia.

You are known for creating engaging trivia questions, and you will be creating a list of questions.

You will create a list of {question_count} questions about this team:

{team1}

Output your question list in a valid JSON format.

Here is an example output. If one of the teams was the UCI Anteaters, the output could look like this:

{question_list_prompt}
"""