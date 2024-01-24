import os
import subprocess


def run_format():
    os.system("black .")
    os.system("isort . --overwrite-in-place")
    os.system("ruff format .")
    # also lints
    run_lint()


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


def run_acceptancetest():
    run_command("pytest -m acceptance")


def run_mutmut():
    run_command("mutmut run")


def run_mutmut_report():
    run_command("mutmut junitxml --suspicious-policy=ignore --untested-policy=ignore")
