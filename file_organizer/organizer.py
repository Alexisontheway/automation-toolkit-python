import shutil
import hashlib
from pathlib import Path


def get_file_hash(file_path: Path, chunk_size: int = 4096) -> str:
    """
    Generate SHA-256 hash for a file using chunked reading.
    """
    hasher = hashlib.sha256()

    with file_path.open("rb") as file:
        while chunk := file.read(chunk_size):
            hasher.update(chunk)

    return hasher.hexdigest()


def organize_by_type(directory_path: str, dry_run: bool = False) -> None:
    """
    Organize files by extension and detect duplicates.
    If dry_run is True, no files are moved.
    """

    directory = Path(directory_path)

    if not directory.exists() or not directory.is_dir():
        print("Invalid directory path.")
        return

    seen_hashes = {}

    for item in directory.iterdir():
        if not item.is_file():
            continue

        file_hash = get_file_hash(item)

        if file_hash in seen_hashes:
            original = seen_hashes[file_hash]
            print(f"[DUPLICATE] {item.name} is a duplicate of {original.name}")

            if dry_run:
                print(f"[DRY-RUN] Would skip duplicate: {item.name}")
            else:
                print(f"Skipping duplicate file: {item.name}")
            continue

        seen_hashes[file_hash] = item

        file_extension = item.suffix.lower().replace(".", "")
        if not file_extension:
            file_extension = "others"

        target_folder = directory / file_extension
        target_folder.mkdir(exist_ok=True)

        destination = target_folder / item.name

        if dry_run:
            print(f"[DRY-RUN] Would move: {item.name} → {target_folder.name}/")
        else:
            shutil.move(str(item), str(destination))
            print(f"Moved: {item.name} → {target_folder.name}/")


if __name__ == "__main__":
    path = input("Enter the directory path to organize: ").strip()
    choice = input("Run in dry-run mode? (yes/no): ").strip().lower()

    dry_run_mode = choice == "yes"
    organize_by_type(path, dry_run=dry_run_mode)
