import statistics

from models.schemas import (
    EvaluationResult,
    ScoreClusteringReport,
    ScoreClusteringResult,
)
from services.bias.base import BiasDetector


class ScoreClusteringDetector(BiasDetector):

    CLUSTER_THRESHOLD = 1.0

    def run(
        self,
        evaluation: EvaluationResult,
    ) -> float:
        """
        Return the overall score for a single evaluation.
        """
        return (
            evaluation.verdict.overall_score_a +
            evaluation.verdict.overall_score_b
        ) / 2

    def evaluate_suite(
        self,
        evaluations: list[EvaluationResult],
    ) -> ScoreClusteringReport:

        scores = []

        for evaluation in evaluations:

            scores.append(
                evaluation.verdict.overall_score_a
            )

            scores.append(
                evaluation.verdict.overall_score_b
            )

        if not scores:

            result = ScoreClusteringResult(
                mean=0.0,
                median=0.0,
                minimum=0.0,
                maximum=0.0,
                variance=0.0,
                standard_deviation=0.0,
                clustered=False,
            )

            return ScoreClusteringReport(
                total_cases=0,
                result=result,
            )

        mean = statistics.mean(scores)

        median = statistics.median(scores)

        minimum = min(scores)

        maximum = max(scores)

        variance = (
            statistics.variance(scores)
            if len(scores) > 1
            else 0.0
        )

        std = (
            statistics.stdev(scores)
            if len(scores) > 1
            else 0.0
        )

        result = ScoreClusteringResult(
            mean=round(mean, 2),
            median=round(median, 2),
            minimum=minimum,
            maximum=maximum,
            variance=round(variance, 2),
            standard_deviation=round(std, 2),
            clustered=std < self.CLUSTER_THRESHOLD,
        )

        return ScoreClusteringReport(
            total_cases=len(evaluations),
            result=result,
        )