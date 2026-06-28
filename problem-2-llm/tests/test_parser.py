from services.loader import TestSuiteLoader
from services.generator import GeneratorService
from services.judge import JudgeService
from services.parser import VerdictParser


def main():

    test_case = TestSuiteLoader.load(
        "data/test_suites/sample_suite.json"
    )[0]

    generator = GeneratorService()

    answer_a = generator.generate(test_case)

    answer_b = "Python is a snake."

    judge = JudgeService()

    raw = judge.judge(
        test_case,
        answer_a,
        answer_b,
    )

    verdict = VerdictParser.parse(raw)

    print("=" * 80)
    print(verdict)
    print("=" * 80)


if __name__ == "__main__":
    main()