import sys

from groq import AsyncGroq
from openai import AsyncOpenAI as OpenAI
from os import getenv
from dotenv import load_dotenv
from sys import exit
from utils.helpers import get_env_path, load_config
from utils.error_notifications import webhook_log, print_error

client = None
model = None


def init_ai():
    global client, model
    env_path = get_env_path()
    config = load_config()

    load_dotenv(dotenv_path=env_path)

    if getenv("OPENAI_API_KEY"):
        client = OpenAI(api_key=getenv("OPENAI_API_KEY"))
        model = config["bot"]["openai_model"]
    elif getenv("GROQ_API_KEY"):
        client = AsyncGroq(api_key=getenv("GROQ_API_KEY"))
        model = config["bot"]["groq_model"]
    else:
        print("No API keys found, exiting.")
        sys.exit(1)


async def generate_response(prompt, instructions, history=None):
    if not client:
        init_ai()
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
        print_error("AI Error", e)
        await webhook_log(None, e)
        return "Sorry, I couldn't generate a response."


async def generate_response_image(prompt, instructions, image_url, history=None):
    if not client:
        init_ai()
    try:
        image_response = await client.chat.completions.create(
            model="llama-3.2-90b-vision-preview",  # [ ] make sure this works when user is using openai
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Describe / Explain in detail this image sent by a Discord user to an AI who will be responding to the message '{prompt}' based on your output as the AI cannot see the image. So make sure to tell the AI any key details about the image that you think are important to include in the response, especially any text on screen that the AI should be aware of.",
                        },
                        {"type": "image_url", "image_url": {"url": image_url}},
                    ],
                }
            ],
        )

        prompt_with_image = (
            f"{prompt} [Image of {image_response.choices[0].message.content}]"
        )

        if history:
            history.append({"role": "user", "content": prompt_with_image})

            response = await client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": instructions
                        + " Images will be described to you, with the description wrapped in [|description|], so understand that you are to respond to the description as if it were an image you can see.",
                    },
                    {"role": "user", "content": prompt_with_image},
                    *history,
                ],
            )
        else:
            history = [{"role": "user", "content": prompt_with_image}]
            response = await client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": instructions},
                    {"role": "user", "content": prompt_with_image},
                ],
            )
        history.append(
            {"role": "assistant", "content": response.choices[0].message.content}
        )
        return response.choices[0].message.content
    except Exception as e:
        print_error("AI Error", e)
        await webhook_log(None, e)
        return "Sorry, I couldn't generate a response."
