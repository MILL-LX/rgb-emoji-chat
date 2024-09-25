import random
import requests
import time
import os

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, send
from flask import send_file

import app_modules.display as display
from app_modules.image_util import images_for_message, image_path_for_image_code, available_image_codes, image_exists_for_code, IMAGE_DIRECTORY_PATH
from app_modules.pi_util import is_raspberry_pi
from app_modules.image_queue_manager import ImageQueueManager

SERVICE_PORT = 3000 if is_raspberry_pi() else 3000#TODO: probably run on port 80 when deployed

app = Flask(__name__)
socketio = SocketIO(app)

display = display.Display()
image_queue_manager = ImageQueueManager(display, socketio)

@app.route('/')
def index():
    return render_template('chat_room.html', methods=['GET'])

# Load the UI for picking the image to display
@app.route('/ImageSelector')
def serve_image_selecctor_ui():
    return render_template('image_selector.html', methods=['GET'])

# Example request: http://peepp-0000.local:3000/AvailableImageCodes
@app.route('/AvailableImageCodes', methods=['GET'])
def avalable_image_codes():
    return jsonify(available_image_codes())

# Example request: http://peepp-0000.local:3000/ShowImage?image_code=MH%20G%20Collection%20PART/8
@app.route('/ShowImage', methods=['GET'])
def show_image():
    image_code = request.args.get('image_code')
    if image_exists_for_code(image_code):
        image_queue_manager.add_image(image_code)
        return jsonify({'status': 'success', 'message': f'Image for code {image_code} queued for display'})
    else:
        return jsonify({'status': 'failure', 'message': f'Image for code {image_code} does not exist'}), 404

# Example request: http://peepp-0000.local:3000/ImageQueueStatus
@app.route('/ImageQueueStatus', methods=['GET'])
def image_queue_status():
    queue_status = image_queue_manager.status()
    return jsonify({'status': 'success', 'queue_status': queue_status})

@app.route('/GetImage', methods=['GET'])
def get_image():
    image_code = request.args.get('image_code')
    image_path = image_path_for_image_code(IMAGE_DIRECTORY_PATH, image_code)
    return send_file(image_path, mimetype='image/png')

def send_to_rgb_sign(msg: str) -> requests.Response:
    sign_host = 'pi-matrix.local' if is_raspberry_pi() else 'localhost'
    sign_url = f'http://{sign_host}/animate/ShowMessage'
    params = {'message': msg}
    try:
        response = requests.get(sign_url, params=params)
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error sending message to RGB sign: {e}")
        return None

@socketio.on('message')
def handle_message(msg):
    send(msg, broadcast=True)
    send_to_rgb_sign(msg)

    msg = msg.upper()
    for image in images_for_message(msg, display.size()):
        display.clear_display()
        time.sleep(0.1)

        if image:
            display.send_image(image)
            time.sleep(0.5)
        else:
            time.sleep(0.25)

if __name__ == '__main__':
    # Seed our random number generator
    random.seed(time.time() + int.from_bytes(os.urandom(4), 'big'))

    display.send_image(images_for_message('🦊', display.size())[0])

    # Start our server
    host = '0.0.0.0' if is_raspberry_pi() else 'localhost'
    socketio.run(app, host=host, port=3000, allow_unsafe_werkzeug=True)
