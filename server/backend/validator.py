import os

def validate_venv():
    if os.environ.get('VIRTUAL_ENV') != os.path.realpath(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.venv')):
        print("Please use the weBlock's server virtual environment to run server scripts.")
        print("Activate with `$ source server/activate` from the repository's root directory.")
        exit(1)

