import os

def validate_venv():
    if not os.environ.get('VIRTUAL_ENV'):
        print("Please use the venv to run server scripts.")
        exit(1)