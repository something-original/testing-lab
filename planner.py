from task import ExtendedTask, GeneralTask
from queue import Queue
from typing import Union

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
            
            if task.priority == 0:
                self.queue_0.put(task)
            elif task.priority == 1:
                self.queue_1.put(task)
            elif task.priority == 2:
                self.queue_2.put(task)
            elif task.priority == 3:
                self.queue_3.put(task)

            self.pick_task(task)       
        else:
            pass

    def pick_task(self, task: Union[GeneralTask, ExtendedTask]):
        
        if self.current_task == None:
            self.current_task = task

        else:
            if self.current_task.priority < task.priority:
                if isinstance(self.current_task, GeneralTask):
                    pass
