import time
import threading
import random
import json
from queue import Queue
import datetime

from flask_socketio import SocketIO

from app_modules.image_util import image_for_code
from app_modules.display import Display
from app_modules.pi_util import is_raspberry_pi

IMAGE_DURATION = 10 #TODO: determine actual image duration

class ImageQueueManager:
    def __init__(self, display: Display, socketio: SocketIO):
        self.image_queue = Queue()
        self.display = display
        self.socketio = socketio

        self.current_image_code = None

        self.running = True
        self.display_thread = threading.Thread(target=self.display_images)
        self.display_thread.start()

    def add_image(self, image_code):
        self.image_queue.put(image_code)

        updated_at = time.time()
        updated_at_str = datetime.datetime.fromtimestamp(updated_at, datetime.timezone.utc).isoformat() + 'Z'  # Use UTC time
        event_data = {
            'event': 'image_queue_updated',
            'event_time': updated_at_str,
            'added_image_code': image_code,
            'current_image_code': self.current_image_code,
            'remaining_image_codes': list(self.image_queue.queue)
        }
        event_data_json = json.dumps(event_data)
        self.socketio.emit('image_updates', event_data_json)

    def display_images(self):
        while self.running:
            if not self.image_queue.empty():
                image_code = self.image_queue.get()
                image = image_for_code(image_code, self.display.size())
                if image:
                    self.current_image_code = image_code
                    self.display.send_image(image)

                    updated_at = time.time()
                    updated_at_str = datetime.datetime.fromtimestamp(updated_at, datetime.timezone.utc).isoformat() + 'Z'  # Use UTC time
                    event_data = {
                        'event': 'image_updated',
                        'event_time': updated_at_str,
                        'event_time': updated_at_str,
                        'current_image_code': self.current_image_code,
                        'remaining_image_codes': list(self.image_queue.queue)
                    }
                    event_data_json = json.dumps(event_data)
                    self.socketio.emit('image_updates', event_data_json)
                    
                    time.sleep(IMAGE_DURATION)

            time.sleep(1)

    def stop(self):
        self.running = False
        self.display_thread.join()

    def status(self):
        return {
            'current_image_code': self.current_image_code,
            'remaining_image_codes': list(self.image_queue.queue)  # Convert Queue to list for easier viewing
        }
