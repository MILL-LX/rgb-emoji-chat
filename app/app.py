import time

from flask import Flask, render_template
from flask_socketio import SocketIO, send
from lib.display import Display
from lib.image_util import images_for_message
from lib.pi_util import is_raspberry_pi

display = Display()
colors = [(255,0,0),(0,255,0),(0,0,255)]
color_index = 0

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(msg):
    send(msg, broadcast=True)

    for image in images_for_message(msg, emoji_only=False):
        display.send_image(image)
        time.sleep(2)

    display.send_image(images_for_message('🦊')[0])

if __name__ == '__main__':
    display.send_image(images_for_message('🦊')[0])

    # Specify the IP address and port
    host = '10.10.10.52' if is_raspberry_pi() else 'localhost'
    socketio.run(app, host=host, port=3000, allow_unsafe_werkzeug=True)
