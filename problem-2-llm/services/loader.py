import json
from pathlib import Path
from typing import List

import yaml

from models.schemas import TestCase


class TestSuiteLoader:
    """Loads and validates test suites from JSON or YAML."""

    @staticmethod
    def load(file_path: str) -> List[TestCase]:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Test suite not found: {file_path}")

        suffix = path.suffix.lower()

        if suffix == ".json":
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

        elif suffix in [".yaml", ".yml"]:
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)

        else:
            raise ValueError(
                "Unsupported file format. Only JSON and YAML are supported."
            )

        if not isinstance(data, list):
            raise ValueError("Test suite must be a list of test cases.")

        return [TestCase.model_validate(item) for item in data]