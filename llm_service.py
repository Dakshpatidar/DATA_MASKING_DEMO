import os

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def get_llm_response(prompt):

    try:

        print("\n========================")
        print("PROMPT SENT TO LLM:")
        print(prompt)
        print("========================\n")

        completion = client.chat.completions.create(

    model="llama-3.3-70b-versatile",

    messages=[

        {
            "role": "system",
            "content": """
You are a helpful AI assistant.

You help users with:
- AI
- Machine Learning
- Coding
- Career guidance
- Projects
- Research

If masked tokens appear like:
[EMAIL_1]
[NAME_1]
[ORG_1]

treat them as normal placeholders.
"""
        },

        {
            "role": "user",
            "content": prompt
        }
    ],

    temperature=0.5,

    max_tokens=1000
)       

        print("\n========================")
        print("RAW COMPLETION:")
        print(completion)
        print("========================\n")

        if (
            not completion.choices
            or completion.choices[0].message.content is None
        ):

            return "LLM did not generate a response."

        response = (
            completion
            .choices[0]
            .message
            .content
        )

        print("\n========================")
        print("FINAL LLM RESPONSE:")
        print(response)
        print("========================\n")

        return response

    except Exception as e:

        print("\n========================")
        print("LLM ERROR:")
        print(str(e))
        print("========================\n")

        return f"LLM ERROR: {str(e)}"