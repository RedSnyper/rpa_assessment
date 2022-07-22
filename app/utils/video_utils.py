from .config import settings
from pathlib import Path
import shutil, os


res_path = settings.storage_root

def delete_entire_folder(user_id):
    folder = Path(Path.cwd(), res_path, user_id)
    shutil.rmtree(folder)

def delete_video_file(file):
    os.remove(file)


def save_video_file(file, file_path):
    filepath = Path(Path.cwd(), file_path, file.filename)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with filepath.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return filepath

def update_video_file(user_id, loc):
    pass