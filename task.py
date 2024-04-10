from enum import Enum
from random import randint
import time
from threading import Thread


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
    len_zeros = 4 - len(id)
    return '0' * len_zeros + id



class GeneralTask():
    def __init__(self, priority, time):
        if priority in [0,1,2,3]:
            self.priority = priority
        else:
            raise ValueError("Приоритет должен быть целым числом от 0 до 3")
        self.state = BaseState.SUSPENDED
        self.id = generate_id()
        self.time_left = time

    state: BaseState
    priority: int
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
            self.start_time = time.time()
            self.state = self.state.RUNNING
            for i in range(0,self.time_left):
              time.sleep(1)
              self.time_left = self.time_left - i
              if self.state == self.state.READY:
                return
            self.terminate()
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

    def run(self):
      Thread(target=self.start)


class ExtendedTask(GeneralTask):
    def __init__(self, priority, finish_time):
        super(ExtendedTask, self).__init__(priority, finish_time)
        self.state = ExtendedState.SUSPENDED

    state: ExtendedState

    def start(self):
        if self.state == self.state.READY:
            self.start_time = time.time()
            self.state = self.state.RUNNING
            for i in range(0,self.time_left):
              time.sleep(1)
              self.time_left = self.time_left - i
              if self.state == self.state.READY or self.state == self.state.WAITING:
                return
            self.terminate()
        else:
            pass


    def wait(self):
        if self.state == self.state.RUNNING:
            self.state = self.state.WAITING
        else:
            pass

    def release(self):
        if self.state == self.state.WAITING:
            self.state = self.state.READY
        else:
            pass

    def run(self):
      Thread(target=self.start)
