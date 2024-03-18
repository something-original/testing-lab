from queue import Queue

from task import GeneralTask


class Planner():
    def __init__(self):
        pass

    queue_0: Queue
    queue_1: Queue
    queue_2: Queue
    queue_3: Queue

    current_task: GeneralTask|None

    def receive_task(self, task: GeneralTask):
        if isinstance(task, GeneralTask):

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

    def pick_task(self, task: GeneralTask):

        if self.current_task is None:
            self.current_task = task

        else:
            if self.current_task.priority < task.priority:
                if type(self.current_task) is GeneralTask:
                    pass
