import os
import logging


def create_dir(dir_path: str):
    exists = os.path.exists(dir_path)
    if not exists:
        os.makedirs(dir_path)


def check_working_dir():
    src_exists = os.path.exists("src")
    app_exists = os.path.exists("app")
    if not src_exists or not app_exists:
        logging.critical("Script is ran from the wrong directory\n"
                         "Could not find ./src or ./app directory.\n"
                         "Please run the script from the repository root using\n"
                         "python src/main.py\n"
                         "or\n"
                         "python app/main.py")
        raise Exception("Critical error. Please read logfile or console for more information")
