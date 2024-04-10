from task import ExtendedTask, GeneralTask
from task import BaseState, ExtendedState
from fifo import Fifo
from threading import Event

import time


class Scheduler():
    def __init__(self, queues: Fifo, event: Event):
        self.queues = queues
        self.event = event

    current_task: None
    queues: Fifo
    event: Event

    def clear(self):
        self.current_task = None


    def pick_task(self):
        while True:
            if self.current_task == None:
                for queue in self.queues.queues.values():
                    if queue.not_empty:
                        self.current_task = queue.get()
                        #self.run_task()
                        break
            else:
                for priority, queue in self.queues.queues.items():
                    if self.current_task.priority < priority and queue.not_empty:
                        self.stop_task()
                        print(f'Задача с {self.current_task.id} остановлена')
                        self.current_task = queue.get()
                        print(f'Выбрана задача с id {self.current_task.id}')
                        #self.run_task()
                        break
            time.sleep(1)


    def stop_task(self):
        self.event.set()
        if type(self.current_task) == GeneralTask:
            self.current_task.terminate()
        if type(self.current_task) == ExtendedTask:
            self.current_task.wait()
        self.queues.receive_task(self.current_task)
        self.event.clear()


    def run_task(self):
        while True:
            if self.current_task == None:
                pass
            if type(self.current_task) == GeneralTask:
                if self.current_task.state == BaseState.SUSPENDED:
                    self.current_task.activate()
                if self.current_task.state == BaseState.READY:
                    self.current_task.start()
                    print(f'Задача с id {self.current_task.id} завершена или приостановлена')
                    self.clear()
            if type(self.current_task) == ExtendedTask:
                if self.current_task.state == ExtendedState.WAITING:
                    self.current_task.release()
                if self.current_task.state == ExtendedState.SUSPENDED:
                    self.current_task.activate()
                if self.current_task.state == ExtendedState.READY:
                    self.current_task.start()
                    print(f'Задача с id {self.current_task.id} завершена или приостановлена')
                    self.clear()           



