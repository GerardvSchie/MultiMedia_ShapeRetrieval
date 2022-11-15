import os
import logging


def check_working_dir() -> None:
    """Sanity check to verify script is ran from the correct directory"""

    # Checks for both src and app folder in current directory
    src_exists = os.path.exists("src")
    app_exists = os.path.exists("app")

    # Raise exception if the script is not ran from the correct directory
    if not src_exists or not app_exists:
        logging.critical("Script is ran from the wrong directory\n"
                         "Could not find ./src or ./app directory.\n"
                         "Please run the script from the repository root using\n"
                         "python src/main.py\n"
                         "or\n"
                         "python app/main.py")
        raise Exception("Critical error. Please read logfile or console for more information")
