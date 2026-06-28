import csv
import json
from pathlib import Path
import os
from datetime import datetime

from models.schemas import EvaluationResult


class ReportGenerator:

    def __init__(self):

        self.output_dir = Path("reports")
        self.output_dir.mkdir(
            exist_ok=True,
        )

    def generate_json(
        self,
        evaluations: list[EvaluationResult],
        metrics: dict,
        bias_reports: dict,
        validation_report,
        filename: str = "evaluation_report.json",
    ):

        report = {
            "metadata": {
                "framework": "LLM Evaluation Framework",
                "version": "1.0",
                "generated_at": datetime.now().isoformat(),
                "generator_model": os.getenv("GENERATOR_MODEL"),
                "judge_model": os.getenv( "JUDGE_MODEL"),
                "total_cases": len(evaluations),
            },

            "metrics": metrics,
            "bias_analysis": bias_reports,
            "judge_validation": validation_report.model_dump(mode="json"),
            "recommendation": {
                "judge_reliable":validation_report.average_consistency>= 95,
                "position_bias":("Low" if bias_reports["position_bias"]["flip_rate"] < 0.1 else "High"),
                "verbosity_bias":("Low" if bias_reports["verbosity_bias"]["verbosity_bias_rate"] < 0.25 else "High"),
                "self_enhancement":bias_reports["self_enhancement_bias"]["risk"],
                "sycophancy":("Low" if bias_reports["sycophancy_bias"]["sycophancy_rate"] < 0.25 else "High"),
                "score_clustering":("Acceptable" if not bias_reports["score_clustering"]["result"]["clustered"] else "Needs Review"),

            },
            "evaluations": [
                evaluation.model_dump(mode="json")
                for evaluation in evaluations
            ],
        }

        path = self.output_dir / filename

        with open(
            path,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                report,
                file,
                indent=4,
                ensure_ascii=False,
            )

        return path

    def generate_csv(
        self,
        evaluations: list[EvaluationResult],
        filename: str = "evaluation_report.csv",
    ):

        path = self.output_dir / filename

        with open(
            path,
            "w",
            newline="",
            encoding="utf-8",
        ) as file:

            writer = csv.writer(file)

            writer.writerow(
                [
                    "Case ID",
                    "Winner",
                    "Score A",
                    "Score B",
                    "Judge Model",
                    "Timestamp",
                    "Answer A",
                    "Answer B",
                ]
            )

            for evaluation in evaluations:

                writer.writerow(
                    [
                        evaluation.test_case.id,

                        evaluation.verdict.winner,

                        evaluation.verdict.overall_score_a,

                        evaluation.verdict.overall_score_b,

                        evaluation.judge_call.judge_model,

                        evaluation.judge_call.timestamp.isoformat(),

                        evaluation.answer_a,

                        evaluation.answer_b,
                    ]
                )

        return path