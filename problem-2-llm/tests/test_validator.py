from pprint import pprint

from services.loader import TestSuiteLoader
from services.evaluator import EvaluationPipeline
from services.validator import JudgeValidator


def main():

    cases = TestSuiteLoader.load(
        "data/test_suites/sample_suite.json"
    )

    pipeline = EvaluationPipeline()

    evaluations = []

    for case in cases:

        evaluations.append(
            pipeline.evaluate(
                case,
                system_prompt_a="Answer in one sentence.",
                system_prompt_b="Answer in three sentences.",
            )
        )

    validator = JudgeValidator()

    report = validator.validate_suite(
        evaluations,
        runs=3,
    )

    pprint(report.model_dump())


if __name__ == "__main__":
    main()