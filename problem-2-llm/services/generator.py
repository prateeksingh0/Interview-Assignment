import os
from dotenv import load_dotenv

from models.ollama_client import OllamaClient
from models.schemas import TestCase
from services.prompt_builder import PromptBuilder

load_dotenv()


class GeneratorService:
    def __init__(self):
        self.client = OllamaClient()
        self.model = os.getenv("GENERATOR_MODEL")

    def generate(
        self,
        test_case: TestCase,
        system_prompt: str | None = None,
    ) -> str:

        if system_prompt is None:
            system_prompt = test_case.system_prompt

        prompt = PromptBuilder.build_generator_prompt(test_case,system_prompt,)

        return self.client.generate(
            model=self.model,
            system_prompt=system_prompt,
            user_prompt=prompt,
        )