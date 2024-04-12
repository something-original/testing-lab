import logging
import random
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
            self.state = self.state.RUNNING

    def run_task(self):
      if self.state == self.state.READY:
        self.start()
        self.start_time = time.time()
        timeIter = self.time_left
        for i in range(timeIter):
          time.sleep(1)
          if self.state == self.state.READY:
            return
          else:
            self.time_left = self.time_left - 1
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
      Thread(target=self.run_task).start()

    def __str__(self):
      return str(self.id)


class ExtendedTask(GeneralTask):
    def __init__(self, priority, finish_time):
        super(ExtendedTask, self).__init__(priority, finish_time)
        self.state = ExtendedState.SUSPENDED

    state: ExtendedState
    activated: bool = False

    def run_task(self):
      if self.state == self.state.READY:
        self.start()
        self.start_time = time.time()
        timeIter = self.time_left
        for i in range(timeIter):
          time.sleep(1)
          if self.state == self.state.READY or self.state == self.state.WAITING:
            return
          else:
            self.time_left = self.time_left - 1
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

    def wait_activate(self):
      self.activated = False
      self.wait()
      time.sleep(random.randint(1,5))
      #Для теста
      #time.sleep(1)
      self.release()
      self.activated=True

    def run(self):
      Thread(target=self.run_task).start()

    def start_waiting(self):
      Thread(target=self.wait_activate).start()
