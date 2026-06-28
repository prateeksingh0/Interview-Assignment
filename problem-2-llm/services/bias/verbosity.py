from models.schemas import (
    EvaluationResult,
    VerbosityBiasReport,
    VerbosityBiasResult,
)
from services.bias.base import BiasDetector


class VerbosityBiasDetector(BiasDetector):

    def run(
        self,
        evaluation: EvaluationResult,
    ) -> VerbosityBiasResult:

        answer_a = evaluation.answer_a
        answer_b = evaluation.answer_b

        length_a = len(answer_a.split())
        length_b = len(answer_b.split())

        winner = evaluation.verdict.winner

        if length_a > length_b:
            longer = "A"
        elif length_b > length_a:
            longer = "B"
        else:
            longer = "Tie"

        length_difference = abs(length_a - length_b)

        if min(length_a, length_b) == 0:
            length_ratio = 0.0
        else:
            length_ratio = round(
                max(length_a, length_b) /
                min(length_a, length_b),
                2,
        )

        preferred = (
            longer != "Tie"
            and winner == longer
        )

        return VerbosityBiasResult(
            winner=winner,

            answer_a_length=length_a,
            answer_b_length=length_b,

            longer_answer=longer,

            preferred_longer_answer=preferred,

            length_difference=length_difference,
            length_ratio=length_ratio,
        )

    def evaluate_suite(
        self,
        evaluations: list[EvaluationResult],
    ) -> VerbosityBiasReport:

        results = []

        longer_wins = 0

        for evaluation in evaluations:

            result = self.run(evaluation)

            results.append(result)

            if result.preferred_longer_answer:
                longer_wins += 1

        total = len(results)

        return VerbosityBiasReport(
            total_cases=total,

            longer_answer_wins=longer_wins,

            verbosity_bias_rate=round(
                longer_wins / total,
                4,
            ) if total else 0.0,

            results=results,
        )