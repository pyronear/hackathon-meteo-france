from pathlib import Path


def get_project_data_folder_dir() -> Path:
    return Path(__file__).parent.parent.parent / "data"
