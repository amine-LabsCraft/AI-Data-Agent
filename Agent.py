import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.getenv("OPENROUTER_API_KEY"))

print("=== Chat avec OpenRouter (Streaming) ===")
while True:
    user_input = input("Vous : ")
    if user_input.lower() in ['quit', 'exit']: break
    if not user_input.strip(): continue
    try:
        stream = client.chat.completions.create(
            model="openai/gpt-oss-120b", 
            messages=[{"role": "user", "content": user_input}], 
            stream=True
        )
        print("AI : ", end="", flush=True)
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end="", flush=True)
        print("\n")
    except Exception as e:
        print(f"Erreur : {e}\n")