from keras.models import load_model as _load_model
import numpy as np
from settings import MODEL_PATH


def load_model():
    return _load_model(MODEL_PATH)


def predict(x):
    model = load_model()
    predictions = model.predict(np.expand_dims(x, axis=0))
    return np.squeeze(predictions, axis=0)
