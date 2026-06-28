from models.schemas import EvaluationResult


class MetricsCalculator:
    PASS_THRESHOLD = 7.0

    @classmethod
    def calculate(cls, results: list[EvaluationResult]) -> dict:

        if not results:
            return {}

        total_cases = len(results)

        wins_a = 0
        wins_b = 0
        ties = 0
        passes = 0

        total_score_a = 0.0
        total_score_b = 0.0

        criterion_totals = {}

        for result in results:

            verdict = result.verdict

            total_score_a += verdict.overall_score_a
            total_score_b += verdict.overall_score_b

            if verdict.winner == "A":
                wins_a += 1

                if verdict.overall_score_a >= cls.PASS_THRESHOLD:
                    passes += 1

            elif verdict.winner == "B":
                wins_b += 1

            else:
                ties += 1

            for criterion in verdict.criteria:

                if criterion.name not in criterion_totals:

                    criterion_totals[criterion.name] = {
                        "score_a": 0.0,
                        "score_b": 0.0,
                    }

                criterion_totals[criterion.name]["score_a"] += criterion.score_a
                criterion_totals[criterion.name]["score_b"] += criterion.score_b

        criterion_averages = {}

        for name, values in criterion_totals.items():

            criterion_averages[name] = {
                "average_score_a": round(
                    values["score_a"] / total_cases,
                    2,
                ),
                "average_score_b": round(
                    values["score_b"] / total_cases,
                    2,
                ),
            }

        return {

            "summary": {
                "total_cases": total_cases,
                "pass_rate": round(
                    passes / total_cases * 100,
                    2,
                ),
            },

            "comparison": {
                "wins_a": wins_a,
                "wins_b": wins_b,
                "ties": ties,

                "win_rate_a": round(
                    wins_a / total_cases * 100,
                    2,
                ),

                "win_rate_b": round(
                    wins_b / total_cases * 100,
                    2,
                ),

                "average_score_a": round(
                    total_score_a / total_cases,
                    2,
                ),

                "average_score_b": round(
                    total_score_b / total_cases,
                    2,
                ),
            },

            "criteria": criterion_averages,
        }