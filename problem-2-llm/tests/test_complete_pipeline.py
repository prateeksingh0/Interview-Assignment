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

    evaluations = [
        pipeline.evaluate(
            case,
            system_prompt_a="Answer in one sentence.",
            system_prompt_b="Answer in three sentences.",
        )
        for case in cases
    ]

    metrics = MetricsCalculator.calculate(evaluations)

    bias = BiasManager().run(evaluations)

    validation = JudgeValidator().validate_suite(
        evaluations
    )

    reporter = ReportGenerator()

    reporter.generate_json(
        evaluations,
        metrics,
        bias,
        validation,
    )

    reporter.generate_csv(
        evaluations,
    )

    print("=" * 80)
    print("✓ Complete pipeline executed successfully.")
    print("=" * 80)


if __name__ == "__main__":
    main()