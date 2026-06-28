import json

from json_repair import repair_json
from pydantic import ValidationError

from models.schemas import JudgeVerdict


class VerdictParser:
    """Repairs, parses and validates judge responses."""

    @staticmethod
    def parse(raw_response: str) -> JudgeVerdict:
        try:
            repaired = repair_json(raw_response)

            data = json.loads(repaired)

            return JudgeVerdict.model_validate(data)

        except ValidationError as e:
            raise ValueError(
                f"Judge response failed schema validation:\n{e}"
            )

        except Exception as e:
            raise ValueError(
                f"Unable to parse judge response:\n{e}"
            )