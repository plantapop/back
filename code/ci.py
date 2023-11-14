import os


def run_format():
    os.system("black .")
    os.system("isort .")
    os.system("ruff format .")


def run_lint():
    os.system("isort --check-only .")
    os.system("ruff check .")
    os.system("pflake8 .")


def run_unittest():
    os.system("pytest -m unit")


def run_integrationtest():
    os.system("pytest -m integration")
