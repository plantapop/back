import os
import subprocess


def run_format():
    os.system("black .")
    os.system("isort .")
    os.system("ruff format .")


def run_command(command):
    result = subprocess.run(command, shell=True)
    if result.returncode != 0 and result.returncode != 5:
        exit(result.returncode)


def run_lint():
    run_command("isort --check-only .")
    run_command("ruff check .")
    run_command("pflake8 .")


def run_unittest():
    run_command("pytest -m unit")


def run_integrationtest():
    run_command("pytest -m integration")