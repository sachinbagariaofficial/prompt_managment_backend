from dotenv import load_dotenv
import httpx
import os
from langchain.prompts import PromptTemplate
from .constants import tone_instructions

load_dotenv()

API_URL = "https://router.huggingface.co/hf-inference/models/mistralai/Mistral-7B-Instruct-v0.3/v1/chat/completions"
HF_TOKEN = os.getenv("HF_TOKEN")

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json",
}


# Create a LangChain PromptTemplate instance for user input
user_prompt_template = PromptTemplate(
    input_variables=["user_input"], template="{user_input}"
)


async def prompt_gen(payload):
    timeout = httpx.Timeout(60)
    temperature = getattr(payload, "temperature", 0.3)
    top_p = getattr(payload, "top_p", 0.4)
    top_k = getattr(payload, "top_k", 1)
    user_input = getattr(payload, "prompt")
    tone = getattr(payload, "tone")

    # Get tone-specific system instruction
    system_instruction = tone_instructions.get(
        tone, "You are a helpful assistant. Respond clearly and helpfully."
    )

    # Render the user prompt using the PromptTemplate
    formatted_prompt = user_prompt_template.format(user_input=user_input)

    messages = [
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": formatted_prompt},
    ]

    # Token control logic
    if temperature < 0.3:
        max_tokens = 80
    elif temperature < 0.7:
        max_tokens = 120
    else:
        max_tokens = 200

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                API_URL,
                headers=headers,
                json={
                    "messages": messages,
                    "model": "mistralai/Mistral-7B-Instruct-v0.3",
                    "temperature": temperature,
                    "top_p": top_p,
                    "top_k": top_k,
                    "max_tokens": max_tokens,
                },
            )
            response.raise_for_status()
            return response.json()
    except httpx.ReadTimeout:
        print("⏰ Request timed out.")
        return {"error": "The model took too long to respond. Try again later."}
