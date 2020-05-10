from Logger import TrainLogger
import time
import numpy as np


def load(filename: str, arg1: int, arg2: float):
    time.sleep(2)


def save(l):
    time.sleep(2)


def get_metrics():
    return {'loss': np.random.randint(0, 10), 'dice': np.random.rand(
    ), 'val_loss': np.random.randint(0, 10), 'val_dice': np.random.rand()}


def train():
    log('Loading samples', target=load, args=('some_file.png', 42, 10.0,))
    time.sleep(1)
    log.init_train(50, 10)
    for _ in range(10):
        time.sleep(np.random.randint(1, 5))
        log.on_epoch_end(get_metrics())
    log('Saving metrics', target=save, args=([1, 2, 3],))


if __name__ == '__main__':
    log = TrainLogger(nb_epochs=10)
    log('info log', mode='INFO')
    log('test log', mode='test')
    train()
