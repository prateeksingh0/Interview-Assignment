import json
from datetime import datetime
from pathlib import Path

from models.schemas import EvaluationResult, JudgeCall


class EvaluationLogger:
    def __init__(self):
        self.log_dir = Path("data/logs")
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def log(
        self,
        result: EvaluationResult,
        generator_model: str,
    ):

        filename = (
            datetime.now().strftime("%Y%m%d_%H%M%S")
            + ".json"
        )

        path = self.log_dir / filename

        log_data = {
            "timestamp": datetime.now().isoformat(),

            "test_case": result.test_case.model_dump(),

            "generator_model": generator_model,

            "judge_model": result.judge_call.judge_model,

            "answer_a": result.answer_a,

            "answer_b": result.answer_b,

            "judge_prompt": result.judge_call.prompt,

            "raw_judge_response": result.judge_call.raw_response,

            "parsed_verdict": result.verdict.model_dump(),
        }

        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                log_data,
                f,
                indent=4,
                ensure_ascii=False,
            )