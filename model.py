from keras.models import load_model as _load_model
import os
import numpy as np


APP_ROOT = os.path.dirname(os.path.abspath(__file__))


def load_model():
    return _load_model(os.path.join(APP_ROOT, 'cifar10_model.h5'))


def predict(x):
    model = load_model()
    predictions = model.predict(np.expand_dims(x, axis=0))
    return np.squeeze(predictions, axis=0)
