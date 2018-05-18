from keras.models import load_model as _load_model


def load_model(filepath):
    return _load_model(filepath)
