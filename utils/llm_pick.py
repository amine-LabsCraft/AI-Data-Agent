import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# Même modèle que ton script qui fonctionne bien (compatible reasoning toggle sur OpenRouter)
MODEL_ID = "openai/gpt-oss-120b"


def pick_llm(level: str):
    """
    Retourne un LLM OpenRouter (via LangChain), avec le raisonnement
    activé ou non selon le niveau demandé.

    Args:
        level (str): "low" (sans raisonnement) ou "high" (avec raisonnement).

    Returns:
        ChatOpenAI: instance configurée.
    """
    level = level.lower()

    if level not in ("low", "high"):
        raise ValueError(f"Unsupported level: {level}. Please choose 'low' or 'high'.")

    llm_kwargs = {
        "base_url": "https://openrouter.ai/api/v1",
        "api_key": os.environ.get("OPENROUTER_API_KEY"),
        "model": MODEL_ID,
        "temperature": 0,
    }

    if level == "high":
        # Active le raisonnement via le champ reasoning d'OpenRouter (comme dans ton script 1)
        llm_kwargs["extra_body"] = {
            "reasoning": {
                "max_tokens": 1024
            }
        }

    return ChatOpenAI(**llm_kwargs)


if __name__ == "__main__":
    print("--- Test sans raisonnement (low) ---")
    llm_low = pick_llm("low")
    response_low = llm_low.invoke("What is the capital of France?")
    print(response_low.content)

    print("\n--- Test avec raisonnement (high) ---")
    llm_high = pick_llm("high")
    response_high = llm_high.invoke("What is the capital of France?")
    print(response_high.content)