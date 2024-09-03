import requests
import time

from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, send

from lib.display import Display
from lib.image_util import images_for_message, image_for_code
from lib.pi_util import is_raspberry_pi

display = Display()
colors = [(255,0,0),(0,255,0),(0,0,255)]
color_index = 0

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ShowImage/<image_code>')
def show_image(image_code):
    image = image_for_code(image_code)
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
    for image in images_for_message(msg):
        display.clear_display()
        time.sleep(0.1)

        if image:
            display.send_image(image)
            time.sleep(0.5)
        else:
            time.sleep(0.25)

if __name__ == '__main__':
    display.send_image(images_for_message('🦊')[0])

    # Specify the IP address and port
    host = '0.0.0.0' if is_raspberry_pi() else 'localhost'
    socketio.run(app, host=host, port=3000, allow_unsafe_werkzeug=True)
