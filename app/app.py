from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, leave_room, send
from lib.display import Display
from lib.image_util import lookup_char_image
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
    image_for_character = lookup_char_image(msg[0])
    display.send_image(image_for_character)
    send(msg, broadcast=True)

if __name__ == '__main__':
    display.send_image(lookup_char_image('🦊'))

    # Specify the IP address and port
    host = '10.10.10.52' if is_raspberry_pi() else 'localhost'
    socketio.run(app, host=host, port=3000, allow_unsafe_werkzeug=True)
