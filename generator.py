from threading import Thread

from task import GeneralTask, ExtendedTask
from random import choice, randint, random
from fifo import Fifo
import time

class Generator():
    def __init__(self, fifo):
        self.fifo = fifo

    fifo: Fifo

    def generate(self):
      while True:
        delay = randint(0, 5)
        is_extended = choice([True, False])
        priority = randint(0, 3)
        time_left = randint(7, 10)
        task = ExtendedTask(priority, time_left) if is_extended else GeneralTask(priority, time_left)
        time.sleep(delay)
        print(f'Создана задача {type(task)}, приоритет {task.priority}, id {task.id}')
        self.fifo.put_task(task)


    def create_task(params: str):
        created_task = None
        task_class = params[0]
        task_priority = int(params[1])
        task_finish_time = int(params[2:])

        if task_class == 'g':
            created_task = GeneralTask(task_priority, task_finish_time)
        elif task_class == 'e':
            created_task = ExtendedTask(task_priority, task_finish_time)
        else:
            raise ValueError("Задача может быть только General(g) или Extended(e)")

        if created_task != None:
            return created_task
        else:
            pass

    def run(self):
      Thread(target=self.generate, daemon=True).start()

