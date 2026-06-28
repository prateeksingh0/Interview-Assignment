from collections import Counter

from models.schemas import (
    EvaluationResult,
    JudgeValidationReport,
    JudgeValidationResult,
)
from services.judge import JudgeService
from services.parser import VerdictParser


class JudgeValidator:

    def __init__(self):

        self.judge = JudgeService()

    def validate(
        self,
        evaluation: EvaluationResult,
        runs: int = 3,
    ) -> JudgeValidationResult:

        winners = []

        for _ in range(runs):

            judge_call = self.judge.judge(
                evaluation.test_case,
                evaluation.answer_a,
                evaluation.answer_b,
            )

            verdict = VerdictParser.parse(
                judge_call.raw_response
            )

            winners.append(
                verdict.winner
            )

        counter = Counter(winners)

        consistent = counter.most_common(1)[0][1]

        rate = round(
            consistent / runs * 100,
            2,
        )

        return JudgeValidationResult(
            winners=winners,

            consistent_runs=consistent,

            total_runs=runs,

            consistency_rate=rate,

            stable=(rate == 100),
        )

    def validate_suite(
        self,
        evaluations: list[EvaluationResult],
        runs: int = 3,
    ) -> JudgeValidationReport:

        results = []

        stable_cases = 0

        total_rate = 0.0

        for evaluation in evaluations:

            result = self.validate(
                evaluation,
                runs,
            )

            results.append(result)

            total_rate += result.consistency_rate

            if result.stable:
                stable_cases += 1

        total = len(results)

        return JudgeValidationReport(
            total_cases=total,

            average_consistency=round(
                total_rate / total,
                2,
            ) if total else 0.0,

            stable_cases=stable_cases,

            results=results,
        )