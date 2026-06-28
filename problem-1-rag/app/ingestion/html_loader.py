from bs4 import BeautifulSoup

from .document import Document


class HTMLLoader:

    def load(self, file_path: str):

        with open(file_path, encoding="utf-8") as f:
            html = f.read()

        soup = BeautifulSoup(html, "html.parser")

        text = soup.get_text(separator="\n")

        return Document(
            content=text,
            metadata={
                "source": file_path,
                "type": "html",
            },
        )