import pytest
from client.client import TranslationClient


@pytest.fixture(scope="module")
def start_server():
    import subprocess
    server_process = subprocess.Popen(
        ["python", "server/server.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    yield
    server_process.terminate()  # Cleanup after tests


def test_integration(start_server):
    server_url = "http://127.0.0.1:5000"
    client = TranslationClient(server_url=server_url, max_retries=5, backoff_factor=2)

    def status_callback(status):
        print(f"Integration Test: Status updated -> {status}")

    try:
        result = client.get_job_status(callback=status_callback)
        assert result in ["completed", "error"], f"Unexpected result: {result}"
        print(f"Integration Test: Final status -> {result}")
    except Exception as e:
        pytest.fail(f"Integration Test: Error -> {e}")
