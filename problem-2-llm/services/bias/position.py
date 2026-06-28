from models.schemas import (
    PositionBiasResult,
    TestCase,
)
from services.bias.base import BiasDetector
from services.judge import JudgeService
from services.parser import VerdictParser
from models.schemas import (
    EvaluationResult,
    PositionBiasReport,
    PositionBiasResult,
)


class PositionBiasDetector(BiasDetector):

    def __init__(self):

        self.judge = JudgeService()

    def run(
        self,
        test_case,
        answer_a,
        answer_b,
    ):

        original_call = self.judge.judge(
            test_case,
            answer_a,
            answer_b,
        )

        original = VerdictParser.parse(
            original_call.raw_response
        )

        reversed_call = self.judge.judge(
            test_case,
            answer_b,
            answer_a,
        )

        reversed_result = VerdictParser.parse(
            reversed_call.raw_response
        )

        normalized = self.normalize_reversed_winner(
            reversed_result.winner
        )

        consistent = (
            original.winner == normalized
        )

        return PositionBiasResult(
            original_winner=original.winner,
            reversed_winner=normalized,
            consistent=consistent,
            flip_rate=0.0 if consistent else 1.0,
        )

    @staticmethod
    def normalize_reversed_winner(winner: str) -> str:
        """
        Convert the winner from the reversed evaluation
        back into the original answer space.
        """

        if winner == "A":
            return "B"

        if winner == "B":
            return "A"

        return "Tie"
    
    def evaluate_suite(
        self,
        evaluations: list[EvaluationResult],
    ) -> PositionBiasReport:

        results = []

        consistent = 0
        flipped = 0

        for evaluation in evaluations:

            result = self.run(
                evaluation.test_case,
                evaluation.answer_a,
                evaluation.answer_b,
            )

            results.append(result)

            if result.consistent:
                consistent += 1
            else:
                flipped += 1

        total = len(results)

        return PositionBiasReport(
            total_cases=total,
            consistent_cases=consistent,
            flipped_cases=flipped,
            flip_rate=round(
                flipped / total,
                4,
            ) if total else 0.0,
            results=results,
        )
    
    def consensus_verdict(
        self,
        result: PositionBiasResult,
    ):
        if result.consistent:
            return result.original_winner

        return "Tie"