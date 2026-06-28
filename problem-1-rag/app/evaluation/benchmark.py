import json
from dataclasses import dataclass
from statistics import mean

from app.pipeline.rag_pipeline import RAGPipeline

from .datasets import EVALUATION_DATASET
from .retrieval_metrics import RetrievalMetrics
from .generation_metrics import GenerationMetrics


@dataclass
class BenchmarkResult:

    question: str

    expected_chunks: list[int]

    retrieved_chunks: list[int]

    recall: float

    precision: float

    mrr: float

    ndcg: float

    faithfulness: float

    answer_relevance: float

    context_precision: float

    latency: float


class Benchmark:

    def __init__(
        self,
        pipeline: RAGPipeline,
    ):

        self.pipeline = pipeline

    def run(self):

        results = []

        for sample in EVALUATION_DATASET:

            response = self.pipeline.ask(
                sample.question
            )

            generation = GenerationMetrics.evaluate(

                question=sample.question,

                answer=response["answer"],

                context=response["context"],
            )

            retrieved_chunks = [

                chunk.metadata["chunk_number"]

                for chunk in response["chunks"]

            ]

            results.append(

                BenchmarkResult(

                    question=sample.question,

                    expected_chunks=sample.expected_chunk_numbers,

                    retrieved_chunks=retrieved_chunks,

                    recall=RetrievalMetrics.recall_at_k(
                        sample.expected_chunk_numbers,
                        retrieved_chunks,
                    ),

                    precision=RetrievalMetrics.precision_at_k(
                        sample.expected_chunk_numbers,
                        retrieved_chunks,
                    ),

                    mrr=RetrievalMetrics.mean_reciprocal_rank(
                        sample.expected_chunk_numbers,
                        retrieved_chunks,
                    ),

                    ndcg=RetrievalMetrics.ndcg(
                        sample.expected_chunk_numbers,
                        retrieved_chunks,
                    ),

                    faithfulness=generation.faithfulness,

                    answer_relevance=generation.answer_relevance,

                    context_precision=generation.context_precision,

                    latency=response["latency"],
                )

            )

        return results

    @staticmethod
    def summary(results):

        return {

            "Recall@k": mean(
                r.recall
                for r in results
            ),

            "Precision@k": mean(
                r.precision
                for r in results
            ),

            "MRR": mean(
                r.mrr
                for r in results
            ),

            "nDCG": mean(
                r.ndcg
                for r in results
            ),

            "Faithfulness": mean(
                r.faithfulness
                for r in results
            ),

            "Answer Relevance": mean(
                r.answer_relevance
                for r in results
            ),

            "Context Precision": mean(
                r.context_precision
                for r in results
            ),

            "Latency": mean(
                r.latency
                for r in results
            ),

            "Questions": len(results),

            "Average Retrieved Chunks": mean(
                len(r.retrieved_chunks)
                for r in results
            )
        }
    



    @staticmethod
    def save(results, summary, path):

        output = {

            "summary": summary,

            "results": [

                result.__dict__

                for result in results

            ],
        }

        with open(path, "w", encoding="utf-8") as file:

            json.dump(
                output,
                file,
                indent=4,
            )

    @staticmethod
    def save_markdown(
        summary,
        results,
        path,
    ):

        with open(path, "w", encoding="utf-8") as file:

            file.write("# Benchmark Report\n\n")

            file.write("## Summary\n\n")

            for key, value in summary.items():

                file.write(
                    f"- **{key}**: {value}\n"
                )

            file.write("\n---\n\n")

            file.write("## Per Question\n\n")

            for result in results:

                file.write(
                    f"### {result.question}\n\n"
                )

                file.write(
                    f"- Recall: {result.recall}\n"
                )

                file.write(
                    f"- Precision: {result.precision}\n"
                )

                file.write(
                    f"- MRR: {result.mrr}\n"
                )

                file.write(
                    f"- nDCG: {result.ndcg}\n"
                )

                file.write(
                    f"- Faithfulness: {result.faithfulness}\n"
                )

                file.write(
                    f"- Answer Relevance: {result.answer_relevance}\n"
                )

                file.write(
                    f"- Context Precision: {result.context_precision}\n"
                )

                file.write(
                    f"- Latency: {result.latency:.2f}s\n\n"
                )