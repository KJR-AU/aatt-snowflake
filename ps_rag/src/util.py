from pathlib import Path
from typing import Union, List, Generator
from PyPDF2 import PdfReader

from docx import Document


def extract_text_from_docx(file_path: str | Path) -> str:
    """
    Extracts and returns all text from a DOCX (Microsoft Word) file.

    Args:
        file_path (str): Path to the .docx file.

    Returns:
        str: The concatenated text from all paragraphs in the document.
    """
    if isinstance(file_path, str):
        file_path = Path(file_path)
    doc = Document(file_path)
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    return "\n".join(paragraphs)

def extract_text_from_pdf(file_path: str | Path) -> str:
    """
    Extracts and returns all text from a PDF file.

    Args:
        file_path (str): Path to the PDF file.

    Returns:
        str: The full extracted text from all pages.
    """
    text_content = []
    if isinstance(file_path, str):
        file_path = Path(file_path)

    with file_path.open("rb") as pdf_file:
        reader = PdfReader(pdf_file)
        num_pages = len(reader.pages)

        for i in range(num_pages):
            page = reader.pages[i]
            text = page.extract_text() or ""
            text_content.append(text)

    return "\n".join(text_content)


def iter_files_in_subpaths(
    root_dir: Union[str, Path],
    subpath_names: List[str]
) -> Generator[Path, None, None]:
    """
    Yield .pdf/.docx files located in specific subpaths under the root directory.
    It will look under root / <first_level> / <subpath_name> and list files
    inside that directory (non-recursively). It does not descend further.

    Args:
        root_dir (Union[str, Path]): Root directory to scan.
        subpath_names (List[str]): Names of subdirectories under each first-level dir
            in which to search files (case-insensitive match).

    Yields:
        Path: Path object for each matching .pdf or .docx file.
    """
    root = Path(root_dir).resolve()

    for sub_dir in subpath_names:
        sub_dir_path = root / sub_dir
        for f in sub_dir_path.iterdir():
            if f.is_file() and f.suffix.lower() in {".pdf", ".docx"}:
                yield f


def chunk_text(text: str, chunk_size: int, overlap: int):
    """
    Yields n-sized chunks from the input text with y-sized overlap.

    Args:
        text (str): The text or document content to chunk.
        chunk_size (int): The size of each chunk (number of characters).
        overlap (int): The number of overlapping characters between chunks.

    Yields:
        str: Each chunk of text.
    """
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        yield text[start:end]
        if end >= text_length:
            break
        start = end - overlap
