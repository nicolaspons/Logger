import os
import time
import sys
from threading import Thread, current_thread
from colorama import init, Fore, Back, Style
from typing import Callable


class ThreadLogger(Thread):
    """ Simple Thread class which will run the given function and return the result of the function """

    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, Verbose=None):
        """ This constructor should always be called with keyword arguments.

        Parameters
        ----------
        group: None
            `group` should be None; reserved for future extension when a ThreadGroup class is implemented.
        target: function
            `target` is the callable object to be invoked by the run() method. Defaults to None, meaning nothing is called.
        name: str
            `name` is the thread name. By default, a unique name is constructed of the form “Thread-N” where N is a small decimal number.
        args: tuple
            `args` is the argument tuple for the target invocation. Defaults to ().
        kwargs: dict
            `kwargs` is a dictionary of keyword arguments for the target invocation. Defaults to {}.
        """
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        """ Method representing the thread’s activity. Returs the function res """
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, *args):
        """ Wait until the thread terminates. This blocks the calling thread until the thread whose join() method is called terminates
        - either normally or through an unhandled exception – or until the optional timeout occurs.
        When the timeout argument is present and not None, it should be a floating point number specifying a timeout for the operation in seconds
        (or fractions thereof). As join() always returns None, you must call is_alive() after join() to decide whether a timeout happened 
        – if the thread is still alive, the join() call timed out.
        When the timeout argument is not present or None, the operation will block until the thread terminates.
        """
        Thread.join(self, *args)
        return self._return


class Logger():
    """ `Logger` class which prints additional information when function are called """

    def __init__(self):
        init()  # for windows users
        self._t = None
        self._w = None

    def __call__(self, s: str, target: Callable = None, args: list = None, mode: str = None):
        """ Calls a given function if provided and displays a string s with a given mode

        Parameters
        ----------
        s : str
            The string which will be displayed
        target : function
            The function to execute
        args: list
            The function's arguments
        mode: str
            The displaying mode
        """
        if target is not None:
            self._t = ThreadLogger(target=target, args=args)
            self._t.start()
            self._w = ThreadLogger(target=self.__waitingAnimation, args=(s,))
            self._w.start()
            res = self._t.join()
            self._w.do_run = False
            self._w.join()
            return res

        else:
            if mode is None or mode.upper() == 'INFO':
                print(Fore.GREEN + '[ INFO ] ' + Fore.RESET + s)
            else:
                print(Fore.BLUE +
                      '[ {} ] '.format(mode.upper()) + Fore.RESET + s)
            return None

    def __waitingAnimation(self, s: str):
        """ Runs a simple animation with a given str `s` during the execution of the function `func`
        called from the `__call__` method

        Parameters
        ----------
        s : str
            The string which will be displayed
        """
        n = 0
        while getattr(self._w, "do_run", True):
            n = n % 3+1
            dots = n*'.'+(3-n)*' '
            sys.stdout.write('\r' + Fore.YELLOW +
                             '[ __ ] ' + Fore.RESET + '{}'.format(s) + dots)
            sys.stdout.flush()
            time.sleep(0.5)
        sys.stdout.write('\r' + Fore.GREEN +
                         '[ OK ] ' + Fore.RESET + '{}\033[K\n'.format(s))
        sys.stdout.flush()


class TrainLogger(Logger):
    """ `TrainLogger` class which inherites from its mother `Logger`.
    It does the same with additional methods used for Deep Learning training purposes
    """

    def __init__(self, nb_epochs: int):
        """ Calls the `__init__` method from its mother, stores the number of epochs `nb_epochs`
        and initializes some internal parameters

        Parameters
        ----------
        nb_epochs: int
            The total number of epochs
        """
        super(TrainLogger, self).__init__()
        self.__nb_epochs = nb_epochs
        self.__epoch = 1
        self.__start_epoch = 0

    def init_train(self, train_size: int, val_size: int):
        """ Displays the number of samples used for the training
        and stores the starting time of the first epoch

        Parameters
        ----------
        train_size: int
            The number of samples used for the training
        val_size: int
            The number of samples used for the validation training
        """
        print(Fore.YELLOW + 'Train on {} samples, validate on {} samples'.format(train_size, val_size))
        print(Fore.BLUE + 'Epoch {}/{}'.format(self.__epoch, self.__nb_epochs))
        self.__start_epoch = time.time()

    def on_epoch_end(self, metrics: dict):
        """ Updates some internal parameters and shows training progress
        with metrics computed for this current epoch

        Parameters
        ----------
        metrics: dict
            A `dict` of metrics (for example: {'loss': 0.832, 'dice': 0.87, 'val_loss': 0.841n 'val_dice': 0.82})
        """
        end_epoch = time.time()
        epoch_duration = int(end_epoch - self.__start_epoch)
        print(Fore.GREEN + 'duration : {}'.format(epoch_duration) +
              '-'.join([' {}: {} '.format(key, value) for (key, value) in metrics.items()]))
        self.__epoch += 1
        if self.__epoch <= self.__nb_epochs:
            print(Fore.BLUE + 'Epoch {}/{}'.format(self.__epoch, self.__nb_epochs))
            self.__start_epoch = end_epoch
