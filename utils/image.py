from PIL import Image, ImageDraw, ImageFont
import io
from app import config


def generate_image(text):
    width = config('width')
    height = config('height')
    extra_char = len(text) - config('increase_after_char')
    if extra_char > 0 :
        width += config('per_char_width') * extra_char

    img = Image.new('RGB', (width, height), 'black')
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype('assets/VarelaRound-Regular.ttf',size=config('font_size',30))
    d.text((width/2, height/2), text, anchor='mm', font=font)
    with io.BytesIO() as output:
        img.save(output, format='JPEG')
        return output.getvalue()
