from task import ExtendedTask, GeneralTask
from queue import Queue

class Planner():
    def __init__(self):
        pass

    queue_0: Queue
    queue_1: Queue
    queue_2: Queue
    queue_3: Queue

    current_task: None

    def receive_task(self, task):
        if isinstance(task, (GeneralTask, ExtendedTask)):
            priority = task.priority

            if priority == 0:
                self.queue_0.put(task)
            elif priority == 1:
                self.queue_1.put(task)
            elif priority == 2:
                self.queue_2.put(task)
            elif priority == 3:
                self.queue_3.put(task)           
        else:
            pass

    def pick_task(self):
        if self.current_task == None:
            pass
        else:
            pass