from pprint import pprint

from services.loader import TestSuiteLoader
from services.evaluator import EvaluationPipeline
from services.bias.verbosity import VerbosityBiasDetector


def main():

    cases = TestSuiteLoader.load(
        "data/test_suites/sample_suite.json"
    )

    pipeline = EvaluationPipeline()

    evaluations = []

    for case in cases:

        evaluation = pipeline.evaluate(
            case,
            system_prompt_a="Answer in one sentence.",
            system_prompt_b="Answer in five detailed sentences.",
        )

        evaluations.append(evaluation)

    detector = VerbosityBiasDetector()

    report = detector.evaluate_suite(
        evaluations
    )

    pprint(report.model_dump())


if __name__ == "__main__":
    main()