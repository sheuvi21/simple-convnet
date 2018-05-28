import numpy as np
from worker.model import get_model


def predict(x):
    model = get_model()
    predictions = model.predict(np.expand_dims(x, axis=0))
    return np.squeeze(predictions, axis=0)
