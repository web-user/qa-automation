
import time
import os
import ffmpeg
import pytest


# def test_search(browser):
# 	browser.get('https://www.python.org')
# 	time.sleep(4)

# 	assert 'Welcome' in browser.title


# def test_insert(db_connection):
# 	# db 
#     db_connection.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)')
#     db_connection.execute('INSERT INTO users (name) VALUES (?)', ('Alice',))
#     db_connection.connection.commit()
#     db_connection.execute('SELECT name FROM users WHERE id=1')
#     user = db_connection.fetchone()
#     assert user[0] == 'Alice'


def test_video_conversion(input_video_path, tmp_path):
    # Шлях до вихідного файлу
    output_video_path = tmp_path / 'output_video.avi'

    # Переконуємося, що директорія для вихідного файлу існує
    output_dir = os.path.dirname(output_video_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        # Виконуємо конвертацію відео з MP4 у AVI
        (
            ffmpeg
            .input(input_video_path)
            .output(str(output_video_path))
            .run(overwrite_output=True)
        )
    except ffmpeg.Error as e:
        stderr = e.stderr.decode() if e.stderr else ''
        pytest.fail(f"FFmpeg error during conversion: {stderr}")
    except Exception as e:
        pytest.fail(f"Unexpected error during conversion: {str(e)}")

    # Перевіряємо, що вихідний файл існує
    assert os.path.exists(output_video_path), f"Вихідний відеофайл не створено: {output_video_path}"

    # Додатково перевіряємо тривалість та інші метадані
    try:
        input_probe = ffmpeg.probe(input_video_path)
        output_probe = ffmpeg.probe(str(output_video_path))
    except ffmpeg.Error as e:
        stderr = e.stderr.decode() if e.stderr else ''
        pytest.fail(f"FFmpeg error during probing: {stderr}")
    except Exception as e:
        pytest.fail(f"Unexpected error during probing: {str(e)}")

    input_duration = float(input_probe['format']['duration'])
    output_duration = float(output_probe['format']['duration'])

    # Дозволяємо невелику похибку у тривалості
    assert abs(input_duration - output_duration) < 0.1, f"Тривалість відео не співпадає: вхідне {input_duration}s, вихідне {output_duration}s"


def test_extract_frame(input_video_path, tmp_path):
    # Шлях до вихідного зображення
    output_image_path = tmp_path / 'frame.jpg'

    try:
        # Витягуємо кадр на 1 секунді
        (
            ffmpeg
            .input(input_video_path, ss=1)
            .output(str(output_image_path), vframes=1)
            .run(overwrite_output=True)
        )
    except ffmpeg.Error as e:
        stderr = e.stderr.decode() if e.stderr else ''
        pytest.fail(f"FFmpeg error during frame extraction: {stderr}")
    except Exception as e:
        pytest.fail(f"Unexpected error during frame extraction: {str(e)}")

    # Перевіряємо, що зображення створено
    assert output_image_path.exists(), f"Кадр не було витягнуто: {output_image_path}"











