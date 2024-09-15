import pytest
import os
from selenium import webdriver
import sqlite3


# Base URL for the mock device API
BASE_URL = "http://127.0.0.1:5000"

import requests

# Define the path to the sample video file
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAMPLE_VIDEO_PATH = os.path.join(PROJECT_DIR, 'sample_video', 'sample.mp4')


@pytest.fixture(scope='session')
def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()



# @pytest.fixture(params=['chrome', 'safari'])
# def browser(request):
# 	if request.param == 'chrome':
# 		driver = webdriver.Chrome()
# 	elif request.param == 'safari':
# 		driver = webdriver.Safari()
# 	else:
# 		raise ValueError(f"Unsupported browser: {request.param}")

# 	yield driver
# 	driver.quit()


@pytest.fixture(scope='module')
def db_connection():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    yield cursor
    conn.close()

@pytest.fixture
def output_video_path(tmp_path):
    return tmp_path / 'output_video.avi'


@pytest.fixture(params=['local', 'remote'])
def input_video_path(request, tmp_path):
    source = request.param
    if source == 'local':
        # Шлях до локального файлу
        local_path = SAMPLE_VIDEO_PATH
        assert os.path.exists(local_path), f"Вхідний відеофайл не існує локально: {local_path}"
        return local_path
    elif source == 'remote':
        # Завантажуємо файл з сервера через API
        remote_file_url = f"http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4"
        local_path = tmp_path / 'input_video_remote.mp4'
        response = requests.get(remote_file_url)
        assert response.status_code == 200, f"Не вдалося завантажити файл з сервера: {response.status_code}"
        with open(local_path, 'wb') as f:
            f.write(response.content)
        return str(local_path)
    else:
        pytest.fail(f"Невідоме джерело файлу: {source}")
























