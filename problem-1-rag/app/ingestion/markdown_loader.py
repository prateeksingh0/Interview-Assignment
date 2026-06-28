from markdown_it import MarkdownIt

from .document import Document


class MarkdownLoader:

    def load(self, file_path):

        with open(file_path, encoding="utf-8") as f:
            markdown = f.read()

        parser = MarkdownIt()

        tokens = parser.parse(markdown)

        text = "\n".join(
            token.content
            for token in tokens
            if token.content
        )

        return Document(
            content=text,
            metadata={
                "source": file_path,
                "type": "markdown",
            },
        )