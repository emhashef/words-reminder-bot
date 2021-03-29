from PIL import Image, ImageDraw, ImageFont
import io
from app import config


def generate_image(text):
    width = config('width',300)
    height = config('height',150)
    extra_char = len(text) - config('increase_after_char',10)
    if extra_char > 0 :
        width += config('per_char_width',10) * extra_char

    img = Image.new('RGB', (width, height), 'black')
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype('assets/VarelaRound-Regular.ttf',size=config('font_size',40))
    d.text((width/2, height/2), text, anchor='mm', font=font)
    with io.BytesIO() as output:
        img.save(output, format='JPEG')
        return output.getvalue()
