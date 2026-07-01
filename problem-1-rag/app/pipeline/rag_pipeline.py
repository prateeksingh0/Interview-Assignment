from app.retrieval.retriever import Retriever
from app.retrieval.context_builder import ContextBuilder
from app.retrieval.prompt_builder import PromptBuilder
from app.generation.llm import LLM
from app.evaluation.runtime_metrics import RuntimeMetrics
from app.evaluation.evaluation_service import EvaluationService



class RAGPipeline:

    def __init__(self):

        self.retriever = Retriever()
        self.context_builder = ContextBuilder()
        self.prompt_builder = PromptBuilder()
        self.llm = LLM()

    def ask(
        self,
        question: str,
    ):

        chunks, retrieval_latency = (
            self.retriever.retrieve(question)
        )

        context = self.context_builder.build(chunks)

        prompt = self.prompt_builder.build(
            context,
            question,
        )

        response = self.llm.generate(prompt)

        evaluation = EvaluationService.evaluate(
            question=question,
            answer=response.answer,
            chunks=chunks,
            context=context,
        )

        return {

            "answer": response.answer,
            "chunks": chunks,
            "context": context,
            "prompt": prompt,
            "latency": response.latency,
            "retrieval_latency": retrieval_latency,
            "runtime_metrics": {

                "avg_similarity": RuntimeMetrics.average_similarity(chunks),

                "highest_similarity": RuntimeMetrics.highest_similarity(chunks),

                "lowest_similarity": RuntimeMetrics.lowest_similarity(chunks),

                "context_length": RuntimeMetrics.context_length(context),

                "answer_length": RuntimeMetrics.answer_length(response.answer),
            },
            "evaluation_metrics": evaluation,
        }