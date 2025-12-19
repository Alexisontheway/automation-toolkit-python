import shutil
from pathlib import Path


def organize_by_type(directory_path: str, dry_run: bool = False) -> None:
    """
    Organize files in the given directory by file extension.
    If dry_run is True, no files are moved.
    """

    directory = Path(directory_path)

    if not directory.exists() or not directory.is_dir():
        print("Invalid directory path.")
        return

    for item in directory.iterdir():
        if item.is_file():
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
