from services.loader import TestSuiteLoader
from services.evaluator import EvaluationPipeline
from services.metrics import MetricsCalculator
from services.bias.manager import BiasManager
from services.validator import JudgeValidator
from services.reporter import ReportGenerator


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

    metrics = MetricsCalculator.calculate(
        evaluations
    )

    bias = BiasManager().run(
        evaluations
    )

    validation = JudgeValidator().validate_suite(
        evaluations
    )

    reporter = ReportGenerator()

    json_path = reporter.generate_json(
        evaluations,
        metrics,
        bias,
        validation,
    )

    csv_path = reporter.generate_csv(
        evaluations,
    )

    print()

    print(json_path)

    print(csv_path)


if __name__ == "__main__":
    main()