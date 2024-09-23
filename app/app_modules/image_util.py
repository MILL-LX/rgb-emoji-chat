import os

from PIL import Image, ImageDraw, ImageFont
from uniseg.graphemecluster import grapheme_clusters

from app_modules.pi_util import is_raspberry_pi

_EMOJI_GLYPHS_DIRECTORY_PATH = 'assets/emoji-glyphs/64x64'
_FONT_PATH = 'assets/fonts/MILL/Canada Type - Screener SC.ttf'

IMAGE_DIRECTORY_PATH = '/mnt/peepp-data/images' if is_raspberry_pi() else f'{os.getcwd()}/assets/images'

def image_exists_for_code(image_code: str) -> bool:
    return os.path.exists(image_path_for_image_code(IMAGE_DIRECTORY_PATH, image_code))

def images_for_message(msg, image_size):
    return [image_for_grapheme(g, image_size) for g in _iterate_graphemes(msg)]

def image_for_code(image_code: str, image_size) -> Image.Image:
    return _load_image_for_code(IMAGE_DIRECTORY_PATH, image_code, image_size)

def available_image_codes():
    excluded_filenames = ['.DS_Store']
    
    image_codes = []

    for root, dirs, files in os.walk(IMAGE_DIRECTORY_PATH):
        for file in files:
            relative_path = os.path.relpath(os.path.join(root, file), IMAGE_DIRECTORY_PATH)
            file_path_without_extension = os.path.splitext(relative_path)[0]
            dirname, basename = os.path.split(file_path_without_extension)
            if basename.startswith('.') or basename in excluded_filenames:
                continue
            image_codes.append({
                'full_code': file_path_without_extension,
                'collection': dirname,
                'code': basename
            })

    return {'available_image_codes': image_codes}

def _load_image_for_code(image_directory: str, image_code: str, image_size) -> Image.Image:
    try:
        image_file = image_path_for_image_code(image_directory, image_code)
        image = Image.open(image_file).convert("RGBA")
        if image.mode == 'RGBA':
            red_background = Image.new("RGBA", image.size, (127, 0, 0, 255))
            image = Image.alpha_composite(red_background, image)

        image = image.convert('RGB')

        if image_size != image.size:
            sampling_filter = Image.LANCZOS if image_size > image.size else Image.BICUBIC
            image = image.resize(image_size, sampling_filter)

    except FileNotFoundError as e:
        image = None

    return image

def image_path_for_image_code(image_directory: str, image_code: str) -> str:
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
