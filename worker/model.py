from rq import Worker
from rq.local import LocalStack
from keras.models import load_model
from settings import MODEL_PATH


class ModelWorker(Worker):
    def work(self, *args, **kwargs):
        model = load_model(MODEL_PATH)
        _models.push(model)
        try:
            super().work(*args, **kwargs)
        finally:
            _models.pop()


def get_model():
    return _models.top


_models = LocalStack()
