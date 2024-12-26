from PyPDF2 import PdfReader
from io import BytesIO
from typing import List

class PDFReader:
    def __init__(self, content: bytes = None) -> None:
        self.pdf_file = None
        self.pdf_reader = None
        if content:
            self.set_pdf_content(content)

    def set_pdf_content(self, content: bytes) -> None:
        if not isinstance(content, bytes):
            raise TypeError("Content must be bytes")
        self.pdf_file = BytesIO(content) 
        self.pdf_reader = PdfReader(self.pdf_file)

    def PDFread(self) -> str:  # Added this method for compatibility
        return self.extract_text()

    def extract_text(self) -> str:
        if not self.pdf_reader:
            raise ValueError("No PDF content set")
            
        return '\n'.join(page.extract_text() for page in self.pdf_reader.pages)

def split_text_into_chunks(text: str, chunk_size: int = 1000) -> List[str]:
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]