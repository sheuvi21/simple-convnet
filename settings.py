import os


APP_ROOT = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(APP_ROOT, 'model/cifar10_model.h5')

IMAGE_SIZE = (32, 32)

LABELS = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']

REDIS_URL = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')

SECRET_KEY = os.getenv('SECRET_KEY', '4V7wkf2e5xeNxCJsd2zn4JC9th96D8')
