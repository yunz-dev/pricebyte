import subprocess



def test_ruff():
    """Run Ruff and fail the test if issues are found."""
    result = subprocess.run(["ruff", "check", "."], capture_output=True, text=True)
    assert result.returncode == 0, (
        f"Ruff found style issues:\n{result.stdout}{result.stderr}"
    )
