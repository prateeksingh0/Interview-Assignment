from dataclasses import dataclass
import re


@dataclass
class GenerationMetricsResult:

    faithfulness: float

    answer_relevance: float

    context_precision: float


class GenerationMetrics:

    @staticmethod
    def faithfulness(
        answer: str,
        context: str,
    ) -> float:

        answer_words = set(

            re.findall(
                r"\w+",
                answer.lower(),
            )
        )

        context_words = set(

            re.findall(
                r"\w+",
                context.lower(),
            )
        )

        if not answer_words:

            return 0.0

        overlap = len(
            answer_words & context_words
        )

        return overlap / len(answer_words)

    @staticmethod
    def answer_relevance(
        question: str,
        answer: str,
    ) -> float:

        question_words = set(

            re.findall(
                r"\w+",
                question.lower(),
            )
        )

        answer_words = set(

            re.findall(
                r"\w+",
                answer.lower(),
            )
        )

        if not question_words:

            return 0.0

        overlap = len(
            question_words & answer_words
        )

        return overlap / len(question_words)


    @staticmethod
    def context_precision(
        answer: str,
        context: str,
    ) -> float:

        answer_words = set(

            re.findall(
                r"\w+",
                answer.lower(),
            )
        )

        context_words = set(

            re.findall(
                r"\w+",
                context.lower(),
            )
        )

        if not context_words:

            return 0.0

        overlap = len(
            answer_words & context_words
        )

        return overlap / len(context_words)


    @classmethod
    def evaluate(
        cls,
        question,
        answer,
        context,
    ):

        return GenerationMetricsResult(

            faithfulness=cls.faithfulness(
                answer,
                context,
            ),

            answer_relevance=cls.answer_relevance(
                question,
                answer,
            ),

            context_precision=cls.context_precision(
                answer,
                context,
            ),
        )