import nox
from subprocess import run, CalledProcessError


@nox.session
def test(session):
    """Run pre-commit, git add, and pytest in sequence."""
    try:
        # Run pre-commit using uv
        session.log("Running pre-commit...")
        run(["uv", "run", "pre-commit"])

        # Stage all changes with git
        session.log("Staging changes...")
        run(["git", "add", "."], check=True)

        # Run pytest using uv
        session.log("Running tests...")
        run(["uv", "run", "pytest"], check=True)

    except CalledProcessError as e:
        session.error(f"Command failed with exit code {e.returncode}")
