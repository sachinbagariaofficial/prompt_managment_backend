import os
from dotenv import load_dotenv
import httpx
import asyncio

load_dotenv()

API_URL = "https://router.huggingface.co/hf-inference/models/mistralai/Mistral-7B-Instruct-v0.3/v1/chat/completions"

# HF_TOKEN = os.getenv("HF_TOKEN")


headers = {
    # "Authorization": f"Bearer {os.environ['HF_TOKEN']}",
    "Content-Type": "application/json",
}


print("6666666666")


async def prompt_gen(payload):
    timeout = httpx.Timeout(60)
    temperature = getattr(payload, "temperature", 0.3)
    top_p = getattr(payload, "top_p", 0.4)
    top_k = getattr(payload, "top_k", 1)
    prompt = getattr(payload, "prompt")

    if temperature < 0.3:
        max_tokens = 80
    elif temperature < 0.7:
        max_tokens = 120
    else:
        max_tokens = 200

    print("payload", temperature, max_tokens)
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                API_URL,
                headers=headers,
                json={
                    "messages": [{"role": "user", "content": prompt}],
                    "model": "mistralai/Mistral-7B-Instruct-v0.3",
                    "temperature": temperature,
                    "top_p": top_p,
                    "top_k": top_k,
                    "max_tokens": max_tokens,
                },
            )
            response.raise_for_status()
            print("response2222", response)
            return response.json()
    except httpx.ReadTimeout:
        print("⏰ Request timed out.")
        return {"error": "The model took too long to respond. Try again later."}
