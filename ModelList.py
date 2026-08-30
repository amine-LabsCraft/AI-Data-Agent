import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.getenv("OPENROUTER_API_KEY"))

# Récupérer la liste des modèles via OpenRouter
models_page = client.models.list()

print("=== Modèles Disponibles sur OpenRouter ===")
for model in models_page.data[:20]: # Affiche les 20 premiers pour ne pas inonder le terminal
    print(f"- {model.id}")