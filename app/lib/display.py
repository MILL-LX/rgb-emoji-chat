from lib.flaschen import Flaschen
import numpy as np
from PIL import Image

# Default Flaschentaschen parameters that map to the original peepp project's configuration
_ft_default_UDP_IP = 'localhost'
_ft_default_UDP_PORT = 1337
_ft_default_height = 64
_ft_default_width = 64
_ft_default_default_layer = 0

class Display:

    def __init__(self, ft: Flaschen=None) -> None:
        if ft is None:
            self._ft = Flaschen(_ft_default_UDP_IP, _ft_default_UDP_PORT, _ft_default_width, _ft_default_height, layer=_ft_default_default_layer)
        else:
            self._ft = ft

    def clear_display(self):
        self.fill_display((0,0,0))

    def fill_display(self, color):
        image = Image.new("RGB", (self._ft.width, self._ft.height), color)
        self.send_image(image)

    def send_image(self, image: Image.Image):
        self._ft.send_array(np.array(image), offset=(0,0,0))
