from pathlib import Path

from .pdf_loader import PDFLoader
from .html_loader import HTMLLoader
from .markdown_loader import MarkdownLoader


class DocumentLoader:

    def __init__(self):

        self.pdf = PDFLoader()

        self.html = HTMLLoader()

        self.md = MarkdownLoader()

    def load(self, file_path):

        extension = Path(file_path).suffix.lower()

        if extension == ".pdf":
            return self.pdf.load(file_path)

        if extension in [".html", ".htm"]:
            return self.html.load(file_path)

        if extension == ".md":
            return self.md.load(file_path)

        raise ValueError(
            f"Unsupported file type: {extension}"
        )