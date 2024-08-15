import os

from PIL import Image, ImageDraw, ImageFont


EMOJI_GLYPHS_PATH = 'assets/64x64'
FONT_PATH = 'assets/fonts/MILL/Canada Type - Screener SC.ttf'

def char_to_hex(character: str) -> str:
    hex_codes = [hex(ord(c)).replace('0x', '') for c in character]
    return '-'.join(hex_codes)

def image_file_for_character(character: str) -> str:
    hex_code = char_to_hex(character)
    return f'{EMOJI_GLYPHS_PATH}/{hex_code}.png'

def lookup_char_image(character: str):
    image_file = image_file_for_character(character)

    try: 
        image = Image.open(image_file)
        image = image.convert('RGB')
    except FileNotFoundError as e:
        # image = create_char_image(characterchar)
        image = None
    
    return image

def emoji_images_for_message(msg):
    return [image for c in msg if (image := lookup_char_image(c)) is not None]

def create_char_image(char: str, image_size=(64,64), font_path: str = None) -> Image.Image:
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
# The following is probable a premature optimization that would let us quickly check is a character had an emjoi glyph PNG
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