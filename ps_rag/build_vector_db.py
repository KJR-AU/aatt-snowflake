from chromadb import HttpClient
from chromadb.errors import NotFoundError
from pathlib import Path
import src.util as util
import uuid
import sys
import os
import logging
from langchain.embeddings import init_embeddings

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)

COLLECTION_NAME = os.getenv("COLLECTION_NAME", "aatt_practice_statements")
DB_HOST = os.getenv("CHROMA_HOST", "localhost")
DB_PORT = os.getenv("CHROMA_PORT", 8000)
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "5000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "1000"))
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "huggingface:all-MiniLM-L6-v2")

logger.info(
    "Starting vector DB build with collection=%s host=%s port=%s chunk_size=%s chunk_overlap=%s embedding_model=%s",
    COLLECTION_NAME,
    DB_HOST,
    DB_PORT,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    EMBEDDING_MODEL,
)

root_dir = Path("./docs")
sub_dirs = [
    "AE/Practice Statements",
    "AI/Practice statements",
    "AV/Practice statements AV",
    "Other/Practice Statements",
    "PC (Consent - Control)/Practice statements"
]
logger.debug("Target root directory: %s", root_dir.resolve())
logger.debug("Sub directories to scan: %s", sub_dirs)

try:
    client = HttpClient(host=DB_HOST, port=DB_PORT)
except NotFoundError:
    logger.error("Unable to reach the chroma server at %s:%s. Ensure the server is running and accessible.", DB_HOST, DB_PORT)
    sys.exit(1)

try:
    client.delete_collection(name=COLLECTION_NAME)
except Exception as e:
    logger.warning("Encountered %s while deleting collection: %s", type(e).__name__, e)

collection = client.get_or_create_collection(name=COLLECTION_NAME)


doc_content = {}
files_to_process = list(util.iter_files_in_subpaths(root_dir, sub_dirs))
logger.info("Found %s files to process.", len(files_to_process))
if not files_to_process:
    logger.warning("No files discovered in %s with configured sub-directories.", root_dir)
embeddings = init_embeddings(EMBEDDING_MODEL)
logger.debug("Embeddings model %s initialized.", EMBEDDING_MODEL)

total_chunks = 0
for i, f in enumerate(files_to_process):
    logger.info("Processing file %s of %s: %s", i + 1, len(files_to_process), f)
    category = f.parent.parent.name
    logger.debug("Detected category '%s' for file %s", category, f)
    match f.suffix:
        case ".pdf":
            text = util.extract_text_from_pdf(f)
        case ".docx":
            text = util.extract_text_from_docx(f)
        case _:
            logger.info("Skipping unsupported file type %s for %s", f.suffix, f)
            continue
    logger.debug("Extracted %s characters from %s", len(text), f)
    if text.count("\n") > 500:
        logger.debug("Collapsing excessive newlines for %s", f)
        text = text.replace("\n", "")
    doc_content[str(f)] = text
    
    if (chunks := list(util.chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP))):
        chunk_count = len(chunks)
        total_chunks += chunk_count
        logger.info("Adding %s chunks for %s", chunk_count, f)
        collection.add(
            ids=[uuid.uuid4().hex for _ in chunks],
            documents=chunks,
            embeddings=embeddings.embed_documents(chunks),
            metadatas=[{"source": f.name, "chunk": i, "category": category, "doctype": f.suffix} for _, i in enumerate(chunks)]
        )
    else:
        logger.warning("No content found in: %s", f)

logger.info("Completed vector DB build: %s files processed, %s chunks added to collection '%s'.", len(files_to_process), total_chunks, COLLECTION_NAME)
