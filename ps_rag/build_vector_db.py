from chromadb import HttpClient
from chromadb.errors import NotFoundError
from pathlib import Path
import src.util as util
import uuid
import sys
import os

COLLECTION_NAME = os.getenv("COLLECTION_NAME", "aatt_practice_statements")
DB_HOST = os.getenv("CHROMA_HOST", "localhost")
DB_PORT = os.getenv("CHROMA_PORT", 8000)
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "250"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_SIZE", "25"))

root_dir = Path("./docs/raw")
sub_dirs = [
    "AE/Practice Statements",
    "AI/Practice statements",
    "AV/Practice statements AV",
    "Other/Practice Statements",
    "PC (Consent - Control)/Practice statements"
]
try:
    client = HttpClient(host=DB_HOST, port=DB_PORT)
except NotFoundError:
    print(f"Unable to reach the chroma server at {DB_HOST}:{DB_PORT} Ensure the server is running and accessible.")
    sys.exit(1)

try:
    client.delete_collection(name=COLLECTION_NAME)
except Exception as e:
    print(f"Encountered {type(e).__name__}: {e}")

collection = client.get_or_create_collection(name=COLLECTION_NAME)


doc_content = {}
files_to_process = list(util.iter_files_in_subpaths(root_dir, sub_dirs))

for i, f in enumerate(files_to_process):
    print(f"Processing file {i+1} of {len(files_to_process)}: {f}")
    category = f.parent.parent.name
    match f.suffix:
        case ".pdf":
            text = util.extract_text_from_pdf(f)
        case ".docx":
            text = util.extract_text_from_docx(f)
        case _:
            continue
    if text.count("\n") > 500:
        text = text.replace("\n", "")
    doc_content[str(f)] = text
    
    if (chunks := list(util.chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP))):
        collection.add(
            ids=[uuid.uuid4().hex for _ in chunks],
            documents=chunks,
            metadatas=[{"source": f.name, "chunk": i, "category": category, "doctype": f.suffix} for _, i in enumerate(chunks)]
        )
    else:
        print(f"No content found in: {f}")
