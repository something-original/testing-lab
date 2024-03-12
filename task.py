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
    len_zeros = 4 - len(id)
    return '0' * len_zeros + id



class GeneralTask():
    def __init__(self, priority, finish_time):
        if priority in [0,1,2,3]:
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
            self.start_time = time.time()
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


class ExtendedTask(GeneralTask):
    def __init__(self, priority):
        super(ExtendedTask, self).__init__(priority)
        self.state = ExtendedState.SUSPENDED

    state: ExtendedState

    def wait(self):
        if self.state == self.state.RUNNING:
            self.current_time = time.time() - self.start_time
            self.time_left = self.finish_time - self.current_time
            self.state = self.state.WAITING
        else:
            pass         

    def release(self):
        if self.state == self.state.WAITING:
            self.state = self.state.READY
        else:
            pass    