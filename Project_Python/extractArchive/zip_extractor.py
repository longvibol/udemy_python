import zipfile
import rarfile
from pathlib import Path

def extract_archive(archive_path, output_path):
    archive_path = Path(archive_path)

    match archive_path.suffix.lower():
        case ".zip":
            with zipfile.ZipFile(archive_path, "r") as archive:
                archive.extractall(output_path)

        case ".rar":
            with rarfile.RarFile(archive_path, "r") as archive:
                archive.extractall(output_path)

        case _:
            raise ValueError("Unsupported archive format")



if __name__ == "__main__":
    extract_archive("archive_path/archive_path.rar", "archive_path")

