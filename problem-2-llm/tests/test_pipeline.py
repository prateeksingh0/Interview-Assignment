from services.loader import TestSuiteLoader
from services.evaluator import EvaluationPipeline


def main():
    print("Loading test suite...")
    test_case = TestSuiteLoader.load(
        "data/test_suites/sample_suite.json"
    )[0]

    print("Creating pipeline...")
    pipeline = EvaluationPipeline()

    print("Starting evaluation...")

    result = pipeline.evaluate(
        test_case,
        system_prompt_a="Answer in exactly one sentence.",
        system_prompt_b="Answer in exactly three sentences.",
    )

    print("Evaluation complete!")

    print("=" * 80)
    print(result)


if __name__ == "__main__":
    main()