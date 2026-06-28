from models.schemas import EvaluationResult, TestCase
from services.generator import GeneratorService
from services.judge import JudgeService
from services.parser import VerdictParser
from services.logger import EvaluationLogger

import os


class EvaluationPipeline:
    def __init__(self):
        self.generator = GeneratorService()
        self.judge = JudgeService()
        self.logger = EvaluationLogger()

    def evaluate(
        self,
        test_case: TestCase,
        system_prompt_a: str | None = None,
        system_prompt_b: str | None = None,
    ) -> EvaluationResult:

        answer_a = self.generator.generate(
            test_case,
            system_prompt_a,
        )

        answer_b = self.generator.generate(
            test_case,
            system_prompt_b,
        )

        judge_call = self.judge.judge(
            test_case,
            answer_a,
            answer_b,
        )

        verdict = VerdictParser.parse(
            judge_call.raw_response
        )

        result = EvaluationResult(
            test_case=test_case,
            answer_a=answer_a,
            answer_b=answer_b,
            verdict=verdict,
            judge_call=judge_call,
        )

        self.logger.log(
            result,
            os.getenv("GENERATOR_MODEL"),
        )

        return result