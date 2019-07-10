from typing import Callable
import abc


class Middleware(abc.ABC):
    def __init__(self):
        self.next_func = None

    def __call__(self, *args, **kwargs):
        check_passed = self.check(*args, **kwargs)
        if check_passed and self.next_func:
            return self.next_func(*args, **kwargs)
        else:
            return self.default()

    def add_next(self, next_func: Callable):
        pointer = self
        while pointer.next_func is not None:
            pointer = pointer.next_func

        pointer.next_func = next_func

        return self

    @abc.abstractmethod
    def default(self):
        pass

    @abc.abstractmethod
    def check(self, *args, **kwargs):
        return False
