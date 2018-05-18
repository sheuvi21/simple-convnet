from PIL import Image
import numpy as np


def preprocess_image(fp):
    im = Image.open(fp)
    im = im.convert('RGB')
    box = ((im.width - min(im.size)) / 2, (im.height - min(im.size)) / 2) + (min(im.size),) * 2
    im = im.crop(box)
    im = im.resize((32, 32), resample=Image.BILINEAR)
    return np.array(im.getdata()).reshape(im.size + (3,)) / 255.0
