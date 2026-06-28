import time
import ollama
import re
from config import settings

from .response import GenerationResponse


class LLM:

    def __init__(self):

        self.model = settings.ollama_model

    def generate(
        self,
        prompt: str,
    ) -> GenerationResponse:

        start = time.perf_counter()

        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a retrieval-augmented AI assistant. "
                        "Always answer ONLY from the supplied context. "
                        "Reason using the retrieved evidence but never invent facts."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            options={
                "temperature": 0.1,
                "top_p": 0.9,
                "num_predict": 512,
            },
        )

        latency = time.perf_counter() - start

        answer = response["message"]["content"]

        return GenerationResponse(
            answer=answer,
            latency=latency,
        )