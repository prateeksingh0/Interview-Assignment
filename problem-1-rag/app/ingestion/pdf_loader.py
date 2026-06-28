import fitz

from .document import Document


class PDFLoader:

    def load(self, file_path: str) -> Document:

        doc = fitz.open(file_path)

        pages = []

        for page in doc:
            pages.append(page.get_text())

        text = "\n".join(pages)

        return Document(
            content=text,
            metadata={
                "source": file_path,
                "type": "pdf",
                "pages": len(doc),
            },
        )