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

LOCAL_DEVELOPMENT_LOGO_IMAGE_CODES = ['1f1e6-1f1eb', '1f3c2-1f3fb']
LOGO_IMAGE_CODES = ['MH G Collection PART/8', 'MH G Collection PART/9']  if is_raspberry_pi() else LOCAL_DEVELOPMENT_LOGO_IMAGE_CODES #TODO: substitute with actual logo image codes
LOGO_IMAGE_DURATION = 2
IMAGE_DURATION = 10 #TODO: determine actual image duration

class ImageQueueManager:
    def __init__(self, display: Display, socketio: SocketIO):
        self.image_queue = Queue()
        self.display = display
        self.socketio = socketio
        logo_image_codes = LOGO_IMAGE_CODES
        self.logo_images = [image_for_code(code, display.size()) for code in logo_image_codes]

        self.current_image_code = None

        self.running = True
        self.display_thread = threading.Thread(target=self.display_images)
        self.display_thread.start()

    def add_image(self, image_code):
        self.image_queue.put(image_code)

    def display_images(self):
        while self.running:
            if not self.image_queue.empty():
                image_code = self.image_queue.get()
                image = image_for_code(image_code, self.display.size())
                if image:
                    self.current_image_code = image_code

                    self.display.send_image(random.choice(self.logo_images)) # randomly select one of the logo images   
                    time.sleep(LOGO_IMAGE_DURATION)

                    self.display.send_image(image)

                    updated_at = time.time()
                    updated_at_str = datetime.datetime.fromtimestamp(updated_at, datetime.timezone.utc).isoformat() + 'Z'  # Use UTC time
                    event_data_json = json.dumps({'event': 'image_updated', 'event_time': updated_at_str, 'image_code': image_code})

                    self.socketio.emit('image_updates', event_data_json)
                    self.socketio.emit('message', event_data_json) #DEBUG: we debug by publishing to the chat room, remove this   
                    
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
