import os

from models.schemas import (
    EvaluationResult,
    SelfEnhancementBiasReport,
    SelfEnhancementBiasResult,
)
from services.bias.base import BiasDetector


class SelfEnhancementBiasDetector(BiasDetector):

    @staticmethod
    def get_family(model_name: str) -> str:

        model_name = model_name.lower()

        if model_name.startswith("llama"):
            return "llama"

        if model_name.startswith("qwen"):
            return "qwen"

        if model_name.startswith("mistral"):
            return "mistral"

        if model_name.startswith("gemma"):
            return "gemma"

        if model_name.startswith("phi"):
            return "phi"

        return "unknown"

    def run(
        self,
        evaluation: EvaluationResult,
    ) -> SelfEnhancementBiasResult:

        generator = os.getenv("GENERATOR_MODEL", "")

        judge = evaluation.judge_call.judge_model

        generator_family = self.get_family(generator)

        judge_family = self.get_family(judge)

        same_family = (
            generator_family == judge_family
        )

        risk = (
            "High"
            if same_family
            else "Low"
        )

        return SelfEnhancementBiasResult(
            generator_model=generator,

            judge_model=judge,

            generator_family=generator_family,

            judge_family=judge_family,

            same_family=same_family,

            risk=risk,
        )

    def evaluate_suite(
        self,
        evaluations: list[EvaluationResult],
    ) -> SelfEnhancementBiasReport:

        results = []

        same_family = 0

        for evaluation in evaluations:

            result = self.run(evaluation)

            results.append(result)

            if result.same_family:
                same_family += 1

        total = len(results)

        overall_risk = (
            "High"
            if same_family > 0
            else "Low"
        )

        return SelfEnhancementBiasReport(
            total_cases=total,

            same_family_cases=same_family,

            risk=overall_risk,

            results=results,
        )