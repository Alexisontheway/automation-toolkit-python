import shutil
import hashlib
import logging
import argparse
from pathlib import Path


# ---------------- LOGGING SETUP ----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


# ---------------- HASHING ----------------
def get_file_hash(file_path: Path, chunk_size: int = 4096) -> str:
    """
    Generate SHA-256 hash for a file using chunked reading.
    """
    hasher = hashlib.sha256()

    with file_path.open("rb") as file:
        while chunk := file.read(chunk_size):
            hasher.update(chunk)

    return hasher.hexdigest()


# ---------------- CORE LOGIC ----------------
def organize_by_type(directory_path: Path, dry_run: bool = False) -> None:
    """
    Organize files by extension and detect duplicates.
    """

    if not directory_path.exists() or not directory_path.is_dir():
        logging.error("Invalid directory path provided.")
        return

    seen_hashes = {}

    for item in directory_path.iterdir():
        if not item.is_file():
            continue

        file_hash = get_file_hash(item)

        # Duplicate detection
        if file_hash in seen_hashes:
            original = seen_hashes[file_hash]
            logging.warning(
                f"Duplicate detected: {item.name} (duplicate of {original.name})"
            )
            continue

        seen_hashes[file_hash] = item

        file_extension = item.suffix.lower().replace(".", "")
        if not file_extension:
            file_extension = "others"

        target_folder = directory_path / file_extension
        target_folder.mkdir(exist_ok=True)

        destination = target_folder / item.name

        if dry_run:
            logging.info(f"[DRY-RUN] Would move {item.name} → {target_folder.name}/")
        else:
            shutil.move(str(item), str(destination))
            logging.info(f"Moved {item.name} → {target_folder.name}/")


# ---------------- CLI INTERFACE ----------------
def parse_arguments():
    parser = argparse.ArgumentParser(
        description="File Organizer with duplicate detection and dry-run support"
    )

    parser.add_argument(
        "path",
        type=Path,
        help="Directory path to organize",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate actions without moving files",
    )

    return parser.parse_args()


# ---------------- ENTRY POINT ----------------
if __name__ == "__main__":
    args = parse_arguments()
    organize_by_type(args.path, dry_run=args.dry_run)
