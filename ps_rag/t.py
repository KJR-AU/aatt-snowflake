from pathlib import Path
from typing import Generator, Union
from pathlib import Path
from snowflake.snowpark import Session
from snowflake.snowpark.file_operation import PutResult  # (optional, for typing)
from pathlib import Path
from typing import Union, List, Generator
from dotenv import load_dotenv

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


def upload_to_stage(
    local_file: Path,
    stage_path: str,
    session: Session,
    overwrite: bool = False,
    auto_compress: bool = False
) -> PutResult:
    """
    Uploads a local file to a Snowflake internal stage via Snowpark.

    Args:
        local_file (Path): Path to the local file to upload.
        stage_path (str): The stage location in Snowflake (e.g. "@my_stage/prefix/").
        session (Session): Snowpark session object.
        overwrite (bool): Whether to overwrite an existing file in the stage.
        auto_compress (bool): Whether Snowflake should compress the file automatically.

    Returns:
        PutResult: The result object from the upload (status, target, etc.)
    """
    # Ensure local_file is a Path
    local_file = Path(local_file)

    if not local_file.is_file():
        raise ValueError(f"Local file does not exist or is not a file: {local_file}")

    # The session.file.put API expects a string path; we pass the local file path and stage prefix
    # Note: stage_path must include the “@stage” prefix, e.g. "@my_stage/folder"
    # The API will append the file name to the stage path if not explicitly included.
    put_results = session.file.put(
        str(local_file),
        stage_path,
        overwrite=overwrite,
        auto_compress=auto_compress
    )

    # Usually put_results is a list; return the first one (or inspect all)
    return put_results[0]


import os
from session import session

root_dir = Path("docs/raw")
sub_dirs = [
    "AE/Practice Statements",
    "AI/Practice statements",
    "AV/Practice statements AV",
    "Other/Practice Statements",
    "PC (Consent - Control)/Practice statements"
]

load_dotenv()
stage = f"@{os.environ.get('SNOWFLAKE_DATABASE')}.{os.environ.get('SNOWFLAKE_SCHEMA')}"
all_files = list(iter_files_in_subpaths(root_dir, sub_dirs))
for f in all_files:
    for extension in [".pdf", ".docx"]:
        if f.suffix == extension:
            stripped_extension = extension.lstrip('.')
            file_type_stage = f"{stage}.{stripped_extension}"
            assurance_type_subdir = f.parents[1].name # AE, AI, AV, Other, PC (Consent - Control)
            assurance_type_stage = f"{file_type_stage}/{assurance_type_subdir}"
            print(f"Uploading {f} to {assurance_type_stage}")
            upload_to_stage(f, assurance_type_stage, session, overwrite=True)
            break

# print(len(all_files))