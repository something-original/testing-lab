import logging
import time
from asyncio import Queue
from random import choice, randint
from threading import Thread

from task import GeneralTask, ExtendedTask

class Generator():
    def __init__(self, fifo):
        self.fifo = fifo

    fifo: Queue

    def generate(self, tasksReq=20):
      tasksCreated=0
      while tasksCreated<tasksReq:
        delay = randint(1, 3)
        is_extended = choice([True, False])
        priority = randint(0, 3)
        time_left = randint(2, 7)
        task = ExtendedTask(priority, time_left) if is_extended else GeneralTask(priority, time_left)
        tasksCreated+=1
        time.sleep(delay)
        logging.info(f'Создана задача {type(task)}, приоритет {task.priority}, id {task.id}, длительность {task.time_left}')
        self.fifo.put(task)


    def run(self):
      Thread(target=self.generate, daemon=True).start()

