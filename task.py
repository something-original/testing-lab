from enum import Enum
from random import randint
import time

class BaseState(Enum):
    READY = 1
    RUNNING = 2
    SUSPENDED = 3

class ExtendedState(Enum):
    READY = 1
    RUNNING = 2
    SUSPENDED = 3
    WAITING = 4


def generate_id():
    id = str(randint(0, 1000))
    return "{:0>4}".format(id)



class GeneralTask():
    def __init__(self, priority: int, finish_time: int):
        if priority in range(4):
            self.priority = priority
        else:
            raise ValueError("Приоритет должен быть целым числом от 0 до 3")
        self.state = BaseState.SUSPENDED
        self.id = generate_id()
        self.finish_time = finish_time

    state: BaseState
    priority: int
    finish_time : int
    current_time : int
    time_left : int
    start_time : int
    id : str

    def activate(self):
        if self.state == self.state.SUSPENDED:
            self.state = self.state.READY
        else:
            pass

    def start(self):
        if self.state == self.state.READY:
            self.start_time = int(time.time())
            self.state = self.state.RUNNING
        else:
            pass

    def preempt(self):
        if self.state == self.state.RUNNING:
            self.state = self.state.READY
        else:
            pass

    def terminate(self):
        if self.state == self.state.RUNNING:
            self.state = self.state.SUSPENDED
        else:
            pass

    def __eq__(self, other):
      if type(other) is type(self):
        return self.__dict__ == other.__dict__
      return False

    def __hash__(self):
      return hash(tuple(sorted(self.__dict__.items())))


class ExtendedTask(GeneralTask):
    def __init__(self, priority: int, finish_time: int):
        super(ExtendedTask, self).__init__(priority,finish_time)
        self.state = ExtendedState.SUSPENDED

    state: ExtendedState

    def wait(self):
        if self.state == self.state.RUNNING:
            self.current_time = int(time.time()) - self.start_time
            self.time_left = self.finish_time - self.current_time
            self.state = self.state.WAITING
        else:
            pass

    def release(self):
        if self.state == self.state.WAITING:
            self.state = self.state.READY
        else:
            pass

    def __eq__(self, other):
      if type(other) is type(self):
        return self.__dict__ == other.__dict__
      return False

    def __hash__(self):
      return hash(tuple(sorted(self.__dict__.items())))
