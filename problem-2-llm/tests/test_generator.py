from services.loader import TestSuiteLoader
from services.generator import GeneratorService


def main():

    loader = TestSuiteLoader()

    cases = loader.load(
        "data/test_suites/sample_suite.json"
    )

    generator = GeneratorService()

    for case in cases:

        print("=" * 80)
        print(f"Test Case {case.id}")
        print("=" * 80)

        answer = generator.generate(case)

        print(answer)
        print()


if __name__ == "__main__":
    main()