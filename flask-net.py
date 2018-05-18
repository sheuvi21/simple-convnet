from flask import Flask
from flask import request, render_template, g
from image import preprocess_image
from model import load_model
import numpy as np
import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

LABELS = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST' and 'image' in request.files:
        im = preprocess_image(request.files['image'].stream)
        model = load_model(os.path.join(APP_ROOT, 'cifar10_model.h5'))
        predictions = model.predict(np.expand_dims(im, axis=0))
        predictions *= 100
        return render_template('main.html', labels=LABELS, predictions=np.squeeze(predictions, axis=0))
    else:
        return render_template('main.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
