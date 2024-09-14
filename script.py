# import os
#
# PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# SAMPLE_VIDEO_PATH = os.path.join(PROJECT_DIR, 'qa_engineer_task/sample_video', 'sample.mp4')
#
# print(SAMPLE_VIDEO_PATH)
#
# import os
# import ffmpeg
#
# # Убедитесь, что путь к ffprobe добавлен
# os.environ['PATH'] += os.pathsep + '/opt/homebrew/bin'
#
# try:
#     probe = ffmpeg.probe(local_file)
#     duration = float(probe['format']['duration'])
# except ffmpeg.Error as e:
#     print(f"ffmpeg probing failed: {str(e)}")
#     pytest.fail(f"ffmpeg probing failed: {str(e)}")
#
#
#
#
# # Укажите путь к ffprobe
# ffmpeg.probe(local_file, cmd='/opt/homebrew/bin/ffprobe')
#
#
# try:
#     with open(SAMPLE_VIDEO_PATH, 'rb') as f:
#         content = f.read()
# except OSError as e:
#     print(f"Failed to open file: {e}")
#
#
# print(f"Using file path: {SAMPLE_VIDEO_PATH}")


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time

driver = webdriver.Chrome()


# Open the Python website


driver.get("http://www.python.org")

title = driver.title

print("Title test:  =======", title)

print("dd===============fgfgfg")

search_bar = driver.find_element(By.NAME, "q")

search_bar.clear()

search_bar.send_keys("getting started with python 234234")

time.sleep(4)

search_bar.send_keys(Keys.RETURN)

# Print the current URL

print(driver.current_url)



# Close the browser window

driver.close()