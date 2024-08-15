from PIL import Image, ImageDraw, ImageFont

def char_to_hex(character: str) -> str:
    hex_codes = [hex(ord(c)).replace('0x', '') for c in character]
    return '-'.join(hex_codes)

def image_file_for_character(character: str) -> str:
    hex_code = char_to_hex(character)
    return f'assets/64x64/{hex_code}.png'

def lookup_char_image(char: str):
    image_file = image_file_for_character(char)

    try: 
        image = Image.open(image_file)
        image = image.convert('RGB')
    except FileNotFoundError as e:
        image = create_char_image(char, font_path='assets/fonts/MILL/Canada Type - Screener SC.ttf')
    
    return image

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
