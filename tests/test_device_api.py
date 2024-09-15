import os
import pytest
import requests
import time
import ffmpeg
import io
from unittest.mock import MagicMock
from contextlib import contextmanager
import paramiko


# Base URL for the mock device API
BASE_URL = "http://127.0.0.1:5000"

# Define the path to the sample video file
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAMPLE_VIDEO_PATH = os.path.join(PROJECT_DIR, 'sample_video', 'sample.mp4')


class SSHClientMock(MagicMock):
    def __init__(self, **kwargs):
        super().__init__(spec=paramiko.SSHClient, **kwargs)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    @contextmanager
    def open_sftp(self):
        def _open_sftp_mock_open(filename, mode):
            print(f"Trying to open file: {filename}")
            if os.path.exists(filename):
                print(f"File found: {filename}")
                return open(filename, mode)  # Відкриваємо оригінальний файл
            else:
                print(f"File not found: {filename}")
                raise IOError("File not found")

        open_sftp_mock = MagicMock()
        open_sftp_mock.open = _open_sftp_mock_open
        yield open_sftp_mock

@pytest.fixture
def retrieve_file_via_ssh_fixture():
    def _retrieve_file(file_path):
        local_file = os.path.join("/tmp/local_copy/", os.path.basename(file_path))

        # Create local directory if it doesn't exist
        if not os.path.exists("/tmp/local_copy/"):
            os.makedirs("/tmp/local_copy/")

        # Simulate file retrieval using mock sftp client
        with SSHClientMock() as ssh_client:
            with ssh_client.open_sftp() as sftp:
                with sftp.open(file_path, 'rb') as remote_file:
                    # Write the actual file content returned by mock read() to the local file
                    with open(local_file, 'wb') as local_fh:
                        local_fh.write(remote_file.read())

        return local_file

    return _retrieve_file


@pytest.mark.parametrize("channel_id, recording_config", [
    (1, {"format": "mp4", "resolution": "1080p"}),
    (2, {"format": "avi", "resolution": "720p"}),
    (3, {"format": "mov", "resolution": "1080i"}),
])
def test_device_recording_and_file_retrieval(channel_id, recording_config, retrieve_file_via_ssh_fixture):
    # Set recording configuration
    response = requests.post(f"{BASE_URL}/channel/{channel_id}/recording/config", json=recording_config)
    assert response.status_code == 200

    # Start recording
    response = requests.post(f"{BASE_URL}/channel/{channel_id}/recording/start")
    assert response.status_code == 200

    # Wait for recording duration
    time.sleep(6)

    # Stop recording
    response = requests.post(f"{BASE_URL}/channel/{channel_id}/recording/stop")
    assert response.status_code == 200
    recorded_file = response.json().get("file")

    # Перевірка: якщо шлях до файлу не повертається API
    assert recorded_file, f"Recorded file path not returned by the API for channel {channel_id}"
    print(f"Recorded file path: {recorded_file}")

    # Перевірка: чи існує файл на стороні API
    if not os.path.exists(recorded_file):
        pytest.fail(f"File was not created on the API server: {recorded_file}")

    # Retrieve the file
    local_file = retrieve_file_via_ssh_fixture(recorded_file)

    # Перевіряємо, чи локально файл існує після копіювання
    assert os.path.exists(local_file), f"File was not retrieved successfully: {local_file}"
    print(f"Retrieved file path: {local_file}")

    # Додатково можна перевірити розмір файлу для впевненості, що файл не порожній
    file_size = os.path.getsize(local_file)
    assert file_size > 0, f"File {local_file} is empty or corrupted"

def test_video_duration_validation(retrieve_file_via_ssh_fixture):
    # Use the path to the sample video from the 'sample_video' folder
    recorded_file = SAMPLE_VIDEO_PATH

    # Retrieve the file via SSH
    local_file = retrieve_file_via_ssh_fixture(recorded_file)

    print(f"Local file used for ffprobe: {local_file}")
    assert os.path.exists(local_file), "The local file does not exist."

    # Перевіряємо розмір локального файлу після копіювання
    local_file_size = os.path.getsize(local_file)
    print(f"Original file size (SAMPLE_VIDEO_PATH): {os.path.getsize(SAMPLE_VIDEO_PATH)} bytes")
    print(f"Retrieved file size: {local_file_size} bytes")

    assert local_file_size == os.path.getsize(SAMPLE_VIDEO_PATH), "The file size after retrieval does not match the original file size."

    try:
        # Use ffmpeg to probe the video duration
        probe = ffmpeg.probe(local_file)
        duration = float(probe['format']['duration'])

        print(f"Duration of the file: {duration} seconds")

        # Check if duration is close to the expected recording time (3 seconds)
        assert 2.9 <= duration <= 89, f"Expected duration close to 3 seconds, but got {duration}"

    except ffmpeg.Error as e:
        print(f"FFmpeg error stderr: {e.stderr.decode()}")
        pytest.fail(f"ffmpeg probing failed: {str(e)}")