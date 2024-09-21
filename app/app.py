import requests
import time

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, send

from app_modules.display import Display
import app_modules.display
from app_modules.image_util import images_for_message, image_for_code
from app_modules.pi_util import is_raspberry_pi

display = Display()
colors = [(255,0,0),(0,255,0),(0,0,255)]
color_index = 0

app = Flask(__name__)
socketio = SocketIO(app)

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
    return jsonify(lib.image_util.available_image_codes())


# Example request: http://peepp-0000.local:3000/ShowImage?image_code=MH%20G%20Collection%20PART/8
@app.route('/ShowImage', methods=['GET'])
def show_image():
    image_code = request.args.get('image_code')
    image = image_for_code(image_code, display.size())
    if image:
        display.send_image(image)

    # Always return success to avoid sniffing for errors
    return jsonify({'status': 'success', 'message': f'Displaying image for code {image_code}'})

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
    display.send_image(images_for_message('🦊', display.size())[0])

    # Specify the IP address and port
    host = '0.0.0.0' if is_raspberry_pi() else 'localhost'
    socketio.run(app, host=host, port=3000, allow_unsafe_werkzeug=True)
