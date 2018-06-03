import numpy as np
import json
from settings import LABELS_PATH
from worker.model import get_model


def predict(x):
    model = get_model()
    predictions = model.predict(np.expand_dims(x, axis=0))
    return np.squeeze(predictions, axis=0)


def get_labels():
    fp = open(LABELS_PATH)
    return json.load(fp)
