import os
from dotenv import load_dotenv

from models.ollama_client import OllamaClient

load_dotenv()


def main():
    client = OllamaClient()

    response = client.generate(
        model=os.getenv("GENERATOR_MODEL"),
        system_prompt="You are a helpful assistant.",
        user_prompt="What is Python? Answer in one sentence.",
    )

    print("\nResponse:\n")
    print(response)


if __name__ == "__main__":
    main()