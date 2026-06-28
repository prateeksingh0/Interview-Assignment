import os
from dotenv import load_dotenv

from models.ollama_client import OllamaClient
from models.schemas import TestCase
from services.prompt_builder import PromptBuilder
from models.schemas import JudgeCall

load_dotenv()


class JudgeService:
    def __init__(self):
        self.client = OllamaClient()
        self.model = os.getenv("JUDGE_MODEL")

    def judge(
        self,
        test_case: TestCase,
        answer_a: str,
        answer_b: str,
    ) -> JudgeCall:

        prompt = PromptBuilder.build_judge_prompt(
            test_case,
            answer_a,
            answer_b,
        )

        response = self.client.generate(
            model=self.model,
            system_prompt="You are an expert evaluation system.",
            user_prompt=prompt,
        )

        return JudgeCall(
            prompt=prompt,
            raw_response=response,
            judge_model=self.model,
        )