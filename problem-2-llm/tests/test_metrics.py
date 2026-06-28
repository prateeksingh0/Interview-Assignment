from services.loader import TestSuiteLoader
from services.evaluator import EvaluationPipeline
from services.metrics import MetricsCalculator


def main():

    cases = TestSuiteLoader.load(
        "data/test_suites/sample_suite.json"
    )

    pipeline = EvaluationPipeline()

    results = []

    for case in cases:

        result = pipeline.evaluate(
            case,
            system_prompt_a="Answer in one sentence.",
            system_prompt_b="Answer in three sentences.",
        )

        results.append(result)

    metrics = MetricsCalculator.calculate(results)

    print("=" * 80)
    print(metrics)
    print("=" * 80)


if __name__ == "__main__":
    main()