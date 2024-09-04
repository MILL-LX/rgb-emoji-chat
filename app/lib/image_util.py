from PIL import Image, ImageDraw, ImageFont
from uniseg.graphemecluster import grapheme_clusters

_EMOJI_GLYPHS_DIRECTORY_PATH = 'assets/emoji-glyphs/64x64'
_FONT_PATH = 'assets/fonts/MILL/Canada Type - Screener SC.ttf'

IMAGE_DIRECTORY_PATH = 'assets/simon/emojyFrame'


def images_for_message(msg, image_size, emoji_only=False):
    return [image_for_grapheme(g, image_size) for g in _iterate_graphemes(msg)]

def image_for_code(image_code: str, image_size) -> Image.Image:
    return _load_image_for_code(IMAGE_DIRECTORY_PATH, image_code, image_size)

def _load_image_for_code(image_directory: str, image_code: str, image_size) -> Image.Image:
    try:
        image_file = _image_path_for_image_code(image_directory, image_code)
        image = Image.open(image_file)
        image = image.convert('RGB')
        if image_size != image.size:
            image.thumbnail(image_size)
    except FileNotFoundError as e:
        image = None
    return image

def _image_path_for_image_code(image_directory: str, image_code: str) -> str:
    return f'{image_directory}/{image_code}.png'

def _grapheme_to_hex(grapheme: str) -> str:
    hex_codes = [hex(ord(c)).replace('0x', '') for c in grapheme]
    return '-'.join(hex_codes)

def _emoji_image_for_grapheme(grapheme: str, image_size) -> Image.Image:
    hex_code = _grapheme_to_hex(grapheme)
    return _load_image_for_code(_EMOJI_GLYPHS_DIRECTORY_PATH, hex_code, image_size)

def image_for_grapheme(grapheme: str, image_size):
    emoji_image = _emoji_image_for_grapheme(grapheme, image_size)
    image = emoji_image if emoji_image else _create_char_image(grapheme, image_size)
    return image

def _iterate_graphemes(msg):
    for grapheme in list(grapheme_clusters(msg)):
        yield grapheme

def _create_char_image(char: str, image_size, font_path: str = _FONT_PATH) -> Image.Image:
    # Image dimensions and border thickness
    img_size = image_size
    border_thickness = 2

    # Create a blank image with a black background
    image = Image.new("RGB", img_size, "black")
    draw = ImageDraw.Draw(image)

    # Load the font
    font_size = 60  # Adjust the font size
    font = ImageFont.truetype(font_path, font_size) if font_path else ImageFont.load_default(font_size=font_size)

    # Calculate the position to center the character
    text_width = draw.textlength(char, font=font)

    text_bbox = draw.textbbox((0, 0), char, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    text_x = (img_size[0] - text_width) // 2
    text_y = (img_size[1] - text_height) // 2

    # Draw the character in white
    draw.text((text_x, text_y), char, font=font, fill="white")

    # Draw the 2-pixel black border (already the background, so this is optional)
    draw.rectangle(
        [border_thickness-1, border_thickness-1, img_size[0]-border_thickness, img_size[1]-border_thickness],
        outline="black",
        width=border_thickness
    )

    return image


##########################################################################################################################
# The following is probable a premature optimization that would let us quickly check if a grapheme had an emjoi glyph PNG
##########################################################################################################################

# def _map_basenames_to_paths(directory_path):
#     basename_to_path = {}
    
#     for filename in os.listdir(directory_path):
#         full_path = os.path.join(directory_path, filename)
#         if os.path.isfile(full_path):
#             basename = os.path.splitext(filename)[0]
#             basename_to_path[basename] = full_path
    
#     return basename_to_path

# def get_emoji_glyph_paths():
#     return _map_basenames_to_paths(EMOJI_GLYPHS_PATH)