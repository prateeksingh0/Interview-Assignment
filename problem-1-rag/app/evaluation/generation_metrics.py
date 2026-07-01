from dataclasses import dataclass
import re


@dataclass
class GenerationMetricsResult:
    faithfulness: float
    answer_relevance: float
    context_precision: float
    exact_match: float
    f1: float


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
        expected_answer,
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

            exact_match=cls.exact_match(
                expected_answer,
                answer,
            ),

            f1=cls.f1_score(
                expected_answer,
                answer,
            ),
        )
        
    @staticmethod
    def _tokens(text: str):

        return re.findall(
            r"\w+",
            text.lower(),
        )
        
    @classmethod
    def exact_match(
        cls,
        expected: str,
        predicted: str,
    ) -> float:

        expected = " ".join(
            cls._tokens(expected)
        )

        predicted = " ".join(
            cls._tokens(predicted)
        )

        return float(
            expected == predicted
        )
        
    @classmethod
    def f1_score(
        cls,
        expected: str,
        predicted: str,
    ) -> float:

        expected_tokens = cls._tokens(expected)

        predicted_tokens = cls._tokens(predicted)

        if not expected_tokens or not predicted_tokens:
            return 0.0

        expected_set = set(expected_tokens)

        predicted_set = set(predicted_tokens)

        common = expected_set & predicted_set

        if not common:
            return 0.0

        precision = len(common) / len(predicted_set)

        recall = len(common) / len(expected_set)

        return (
            2 * precision * recall
        ) / (
            precision + recall
        )