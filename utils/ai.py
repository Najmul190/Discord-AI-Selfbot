from groq import AsyncGroq
from os import getenv
from dotenv import load_dotenv

load_dotenv(dotenv_path="config/.env")

client = AsyncGroq(api_key=getenv("GROQ_API_KEY"))


async def generate_response(prompt, instructions, history=None):
    try:
        if history:
            response = await client.chat.completions.create(
                model="llama3-groq-70b-8192-tool-use-preview",
                messages=[
                    {"role": "system", "content": instructions},
                    {"role": "user", "content": prompt},
                    *history,
                ],
            )
        else:
            response = await client.chat.completions.create(
                model="llama3-groq-70b-8192-tool-use-preview",
                messages=[
                    {"role": "system", "content": instructions},
                    {"role": "user", "content": prompt},
                ],
            )

        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating response: {e}")
        return "Sorry, I couldn't generate a response."
