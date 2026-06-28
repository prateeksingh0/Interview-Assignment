from services.loader import TestSuiteLoader


def main():
    test_cases = TestSuiteLoader.load(
        "data/test_suites/sample_suite.json"
    )

    print("=" * 50)

    print(f"Loaded {len(test_cases)} test cases")

    print("=" * 50)

    for case in test_cases:
        print(case)

    print("=" * 50)


if __name__ == "__main__":
    main()