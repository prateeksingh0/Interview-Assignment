from app.evaluation.benchmark_dataset import (
    EVALUATION_DATASET,
)

from app.evaluation.retrieval_metrics import (
    RetrievalMetrics,
)

from app.evaluation.generation_metrics import (
    GenerationMetrics,
)


class EvaluationService:

    @staticmethod
    def evaluate(
        question,
        answer,
        chunks,
        context,
    ):

        sample = next(
            (
                sample
                for sample in EVALUATION_DATASET
                if sample.question.lower().strip()
                == question.lower().strip()
            ),
            None,
        )

        if sample is None:
            return None

        expected = sample.expected_chunk_numbers

        retrieved = [
            chunk.metadata["chunk_number"]
            for chunk in chunks
        ]

        return {

            "expected_answer": sample.expected_answer,

            "recall": RetrievalMetrics.recall_at_k(
                expected,
                retrieved,
            ),

            "precision": RetrievalMetrics.precision_at_k(
                expected,
                retrieved,
            ),

            "mrr": RetrievalMetrics.mean_reciprocal_rank(
                expected,
                retrieved,
            ),

            "ndcg": RetrievalMetrics.ndcg(
                expected,
                retrieved,
            ),

            "faithfulness": GenerationMetrics.faithfulness(
                answer,
                context,
            ),

            "answer_relevance": GenerationMetrics.answer_relevance(
                sample.expected_answer,
                answer,
            ),

            "context_precision": GenerationMetrics.context_precision(
                answer,
                context,
            ),
        }