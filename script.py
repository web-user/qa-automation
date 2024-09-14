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
