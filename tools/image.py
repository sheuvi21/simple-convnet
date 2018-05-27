from PIL import Image
import numpy as np
from settings import IMAGE_SIZE


def preprocess_image(fp):
    im = Image.open(fp)
    im = im.convert('RGB')
    side = min(im.size)
    x = (im.width - side) / 2
    y = (im.height - side) / 2
    square = (x, y) + (side,) * 2
    im = im.crop(square)
    im = im.resize(IMAGE_SIZE, resample=Image.BILINEAR)
    data = np.array(im.getdata())
    data = data.reshape(im.size + (3,))
    data = data / 255.0
    return data
