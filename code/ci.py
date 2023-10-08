import os


def run_black():
    # Execute black
    os.system("black .")
    os.system("isort --profile black --filter-files --skip-glob '*migrations*' .")


def run_pylint():
    # Execute pylint
    os.system("pylint --disable=C0114,C0115,C0116,R0903 plantapop")


def run_pytest():
    # Execute pytest
    os.system("pytest -m unit")
