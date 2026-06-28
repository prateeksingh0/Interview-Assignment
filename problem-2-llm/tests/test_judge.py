from services.loader import TestSuiteLoader
from services.generator import GeneratorService
from services.judge import JudgeService


def main():

    loader = TestSuiteLoader()

    test_case = loader.load(
        "data/test_suites/sample_suite.json"
    )[0]

    generator = GeneratorService()

    answer_a = generator.generate(test_case)

    answer_b = (
        "Python is a snake that lives in forests."
    )

    judge = JudgeService()

    verdict = judge.judge(
        test_case,
        answer_a,
        answer_b,
    )

    print("=" * 80)
    print(verdict)
    print("=" * 80)


if __name__ == "__main__":
    main()