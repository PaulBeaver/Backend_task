import os
import subprocess

import pytest

from ..functions import wait_for_postgres


@pytest.fixture(scope="session", autouse=True)
def start_postgres_container():
    try:
        subprocess.run(
            [
                "docker",
                "compose",
                "-f",
                "docker-compose-tests.yml",
                "up",
                "-d",
                "--build",
                "--force-recreate",
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        wait_for_postgres()

        env = dict(os.environ)
        env["PYTEST"] = "1"

        subprocess.run(["alembic", "upgrade", "head"], env=env)
        yield
    finally:
        try:
            subprocess.run(
                ["docker", "compose", "-f", "docker-compose-tests.yml", "down"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except subprocess.CalledProcessError as e:
            pass
