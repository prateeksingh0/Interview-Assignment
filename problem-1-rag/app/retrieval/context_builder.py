from typing import List
from pathlib import Path
from .models import RetrievedChunk


class ContextBuilder:

    def build(self, chunks):

        context = []

        for chunk in chunks:

            source = Path(
                chunk.metadata["source"]
            ).name

            context.append(
                f"""{chunk.citation}

                {chunk.text}
                """
            )

        return "\n\n".join(context)