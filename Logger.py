import os
import time
import sys
import threading
from colorama import init, Fore, Back, Style


class Logger():
    def __init__(self):
        init()  # for windows users
        self.__t = None

    def __call__(self, s=None):
        if s is None:
            self.__t.do_run = False
            self.__t.join()
        elif type(s) is str:
            self.__t = threading.Thread(
                target=self.__waitingAnimation, args=(s,))
            self.__t.start()

    def update_train(self):
        print(Fore.BLUE + 'Epoch {}/{}'.format(self.epoch, self.nb_epochs))

    def train(self, nb_epochs, nb_samples):
        self.nb_epochs = nb_epochs
        self.nb_samples = nb_samples
        self.epoch = 0
        self.update_train()
        self.__t = threading.Thread(target=self.__trainingAnimation, args=())
        self.__t.start()

    @staticmethod
    def __trainingAnimation(s):  # must be updated to be like a usual keras training
        n = 0
        t = threading.current_thread()
        while getattr(t, "do_run", True):
            n = n % 3+1
            dots = n*'.'+(3-n)*' '
            sys.stdout.write('\r' + Fore.YELLOW +
                             '[ __ ] ' + Fore.RESET + '{}'.format(s) + dots)
            sys.stdout.flush()
            time.sleep(0.5)
        sys.stdout.write('\r' + Fore.GREEN +
                         '[ OK ] ' + Fore.RESET + '{}\033[K\n'.format(s))
        sys.stdout.flush()

    @staticmethod
    def __waitingAnimation(s):
        n = 0
        t = threading.current_thread()
        while getattr(t, "do_run", True):
            n = n % 3+1
            dots = n*'.'+(3-n)*' '
            sys.stdout.write('\r' + Fore.YELLOW +
                             '[ __ ] ' + Fore.RESET + '{}'.format(s) + dots)
            sys.stdout.flush()
            time.sleep(0.5)
        sys.stdout.write('\r' + Fore.GREEN +
                         '[ OK ] ' + Fore.RESET + '{}\033[K\n'.format(s))
        sys.stdout.flush()

    def test(self):
        print(Fore.RED + 'some red text')
        print(Back.GREEN + 'and with a green background')
        print(Style.DIM + 'and in dim text')
        print(Style.RESET_ALL)
        print('back to normal now')


def range_with_status(total):
    """ iterate from 0 to total and show progress in console """
    n = 0
    while n < total:
        done = '#'*(n+1)
        todo = '-'*(total-n-1)
        s = '<{0}>'.format(done+todo)
        if n > 0:
            s = '\r'+s
        print(s, end='')
        yield n
        n = (n+1) % total
