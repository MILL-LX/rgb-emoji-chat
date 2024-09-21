import time
import threading
import random
from queue import Queue

from app_modules.image_util import image_for_code
from app_modules.display import Display

class ImageQueueManager:
    def __init__(self, display: Display):
        self.image_queue = Queue()

        logo_image_codes = ['MH G Collection PART/8', 'MH G Collection PART/9'] #TODO: substitute with actual logo image codes
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
                    self.display.send_image(image)
                    time.sleep(30)
                    self.display.send_image(random.choice(self.logo_images)) # randomly select one of the logo images   
                    time.sleep(10)
                    if self.image_queue.empty():
                        self.display.send_image(image)

            time.sleep(1)

    def stop(self):
        self.running = False
        self.display_thread.join()

    def status(self):
        return {
            'current_image_code': self.current_image_code,
            'remaining_image_codes': list(self.image_queue.queue)  # Convert Queue to list for easier viewing
        }
