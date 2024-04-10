from queue import Queue
from typing import Union
from task import GeneralTask, ExtendedTask

class Fifo():
    def __init__(self, queue_max_len):
        self.queues = {
            3 : Queue(queue_max_len),
            2 : Queue(queue_max_len),
            1 : Queue(queue_max_len),
            0 : Queue(queue_max_len)
        }

    def put_task(self, task: Union[GeneralTask, ExtendedTask]):
        if self.queues[task.priority].not_full:
            self.queues[task.priority].put(task)
            print(f'Задача с id {task.id} принята в очередь приоритета {task.priority}')
        else:
            print(f"Очередь приоритета {task.priority} заполнена")

    def __str__(self):
      return [queue.qsize() for queue in self.queues.values()].__str__()

