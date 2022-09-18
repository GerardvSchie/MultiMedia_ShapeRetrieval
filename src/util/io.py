import os


def create_dir(dir_path: str):
    exists = os.path.exists(dir_path)
    if not exists:
        os.makedirs(dir_path)
