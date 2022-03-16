import os

def validate_venv():
    if os.environ.get('VIRTUAL_ENV') != os.path.realpath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'venv')):
        print("Please use the right venv to run server scripts.")
        exit(1)