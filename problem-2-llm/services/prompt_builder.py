from models.schemas import TestCase


class PromptBuilder:
    @staticmethod
    def build_generator_prompt(
        test_case: TestCase,
        system_prompt: str,
    ) -> str:
        return f"""
            Question:
            {test_case.input}

            Instructions:
            {system_prompt}
            """.strip()

    @staticmethod
    def build_judge_prompt(
        test_case: TestCase,
        answer_a: str,
        answer_b: str,
    ) -> str:

        expected = (
            test_case.expected_output if test_case.expected_output else "Not provided"
        )

        criteria = test_case.criteria or [
            "Correctness",
            "Faithfulness",
            "Completeness",
            "Instruction Following",
            "Tone",
            "Safety",
        ]

        rubric = "\n".join(f"- {criterion}" for criterion in criteria)

        return f"""
You are an impartial AI judge.

Your task is to compare TWO answers.

Evaluate ONLY using the information provided.

Do NOT favor:
- Longer answers
- Better writing style
- More confident wording

Focus only on factual quality and instruction following.

Question:
{test_case.input}

System Prompt:
{test_case.system_prompt}

Expected Answer:
{expected}

Answer A:
{answer_a}

Answer B:
{answer_b}

Evaluate using these criteria:

{rubric}

For EACH criterion:

- Give score_a (0-10)
- Give score_b (0-10)
- Decide winner (A, B, or Tie)
- Explain the reason briefly

Finally determine:

- overall winner
- overall_score_a
- overall_score_b
- overall_rationale

Return ONLY valid JSON.

Use EXACTLY this schema:

{{
    "winner":"A",
    "overall_score_a":0,
    "overall_score_b":0,
    "criteria":[
        {{
            "name":"Correctness",
            "score_a":0,
            "score_b":0,
            "winner":"A",
            "rationale":"..."
        }}
    ],
    "overall_rationale":"..."
}}

Rules:

- Do NOT return Markdown.
- Do NOT wrap JSON inside ``` blocks.
- Return ONLY JSON.
- Every criterion must appear exactly once.
- Scores must be between 0 and 10.
""".strip()
