import os
import time
from datetime import datetime

from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample recording configuration per channel
recording_config = {
	'1': {"format": "mp4", "resolution": "1080p"},
	'2': {"format": "avi", "resolution": "720p"},
	'3': {"format": "mp4", "resolution": "1080p"}
}
recording_state = {'1': 'stopped', '2': 'stopped', '3': 'stopped'}
recording_files = []


@app.route('/channel/<int:id>/recording/config', methods=['GET'])
def get_recording_config(id):
	config = recording_config.get(str(id), {})
	return jsonify(config), 200


@app.route('/channel/<int:id>/recording/config', methods=['POST'])
def config_recording(id):
	global recording_config
	recording_config[str(id)] = request.json
	return jsonify({"status": "config set"}), 200


@app.route('/channel/<int:id>/recording/files', methods=['GET'])
def get_recording_files(id):
	channel_files = [file for file in recording_files if f"/{id}/" in file]
	return jsonify(channel_files), 200


@app.route('/channel/<int:id>/recording/start', methods=['POST'])
def start_recording(id):
	if id in recording_state and recording_state[id] == "recording":
		return jsonify({"status": "already recording"}), 400
	recording_state[id] = "recording"
	return jsonify({"status": "recording started"}), 200


@app.route('/channel/<int:id>/recording/stop', methods=['POST'])
def stop_recording(id):
	if id not in recording_state or recording_state[id] != "recording":
		return jsonify({"status": "not recording"}), 400

	recording_state[id] = "stopped"
	timestamp_start = int(time.time()) - 3600
	timestamp_end = int(time.time())
	file_format = recording_config.get(str(id), {}).get("format", "mp4")
	date_str = datetime.now().strftime("%Y-%m-%d")
	file_path = f"/tmp/recordings/{id}/{date_str}/{timestamp_start}-{timestamp_end}.{file_format}"

	# Ensure the directory exists
	os.makedirs(os.path.dirname(file_path), exist_ok=True)

	# Динамічний розмір файлу на основі тривалості запису
	duration_seconds = timestamp_end - timestamp_start  # Розрахунок тривалості запису в секундах
	bytes_per_second = 500000  # Наприклад, 500KB/с
	file_size = duration_seconds * bytes_per_second  # Розмір файлу залежить від тривалості

	# Створюємо фіктивний файл для тесту з динамічним розміром
	with open(file_path, 'wb') as f:
		f.write(b"\x00" * file_size)  # Створюємо файл з розміром на основі тривалості запису

	recording_files.append(file_path)
	return jsonify({"status": "recording stopped", "file": file_path}), 200


if __name__ == '__main__':
	app.run(debug=True)
