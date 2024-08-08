from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, leave_room, send
from lib.display import Display
from lib.image_util import lookup_char_image

display = Display()
colors = [(255,0,0),(0,255,0),(0,0,255)]
color_index = 0

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

@app.route('/')
def index():
    display.clear_display()
    return render_template('index.html')

@socketio.on('message')
def handle_message(msg):
    image_for_character = lookup_char_image(msg[0])
    display.send_image(image_for_character)
    send(msg, broadcast=True)

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    send(f'{username} has entered the room.', to=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(f'{username} has left the room.', to=room)

if __name__ == '__main__':
    image_for_character = lookup_char_image('🦊')
    display.send_image(image_for_character)

    # Specify the IP address and port
    socketio.run(app, host='10.10.10.52', port=3000)
