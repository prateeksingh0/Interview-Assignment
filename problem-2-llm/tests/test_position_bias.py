from pprint import pprint

from services.loader import TestSuiteLoader
from services.generator import GeneratorService
from services.bias.position import PositionBiasDetector


def main():

    case = TestSuiteLoader.load(
        "data/test_suites/sample_suite.json"
    )[0]

    generator = GeneratorService()

    answer_a = generator.generate(
        case,
        "Answer in one sentence."
    )

    answer_b = generator.generate(
        case,
        "Answer in three sentences."
    )

    detector = PositionBiasDetector()

    result = detector.run(
        case,
        answer_a,
        answer_b,
    )

    pprint(result.model_dump())


if __name__ == "__main__":
    main()