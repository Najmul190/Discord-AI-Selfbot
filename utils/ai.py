from groq import AsyncGroq
from openai import AsyncOpenAI as OpenAI
from os import getenv
from dotenv import load_dotenv
from sys import exit

load_dotenv(dotenv_path="config/.env")

if getenv("OPENAI_API_KEY"):
    client = OpenAI(api_key=getenv("OPENAI_API_KEY"))
    model = "gpt-4o"  # "gpt-4o-mini" for cheaper model
elif getenv("GROQ_API_KEY"):
    client = AsyncGroq(api_key=getenv("GROQ_API_KEY"))
    model = "llama3-70b-8192"
else:
    print("No API keys found, exiting.")
    exit(1)


async def generate_response(prompt, instructions, history=None):
    try:
        if history:
            response = await client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": instructions},
                    {"role": "user", "content": prompt},
                    *history,
                ],
            )
        else:
            response = await client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": instructions},
                    {"role": "user", "content": prompt},
                ],
            )

        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating response: {e}")
        return "Sorry, I couldn't generate a response."
