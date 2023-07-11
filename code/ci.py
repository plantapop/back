import os


def run_black():
    # Execute black
    os.system("black .")


def run_pylint():
    # Execute pylint
    os.system("pylint --disable=C0114,C0116 plantapop")


def run_pytest():
    # Execute pytest
    os.system("pytest -m unit")
