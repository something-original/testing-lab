import logging
from queue import Empty
from typing import Set

from task import ExtendedTask, GeneralTask
from task import BaseState, ExtendedState
from fifo import Fifo
from threading import Event, Thread

import time


class Scheduler():
    def __init__(self, queues: Fifo):
        self.queues = queues
        self.current_task = None
        self.sleeping_tasks = set()

    current_task: None|GeneralTask|ExtendedTask
    queues: Fifo
    sleeping_tasks: Set[ExtendedTask]

    def clear(self):
        self.current_task = None


    def pick_task(self):
      try:
        while True:
          if self.current_task and ((type(self.current_task) == GeneralTask and self.current_task.state!=BaseState.RUNNING) or (type(self.current_task) == ExtendedTask and self.current_task.state!=ExtendedState.RUNNING)):
            logging.info(f"Убрана из выполнения задача {self.current_task.id}")
            self.current_task = None
          if self.current_task is None:
            for queue in self.queues.queues.values():
              try:
                self.current_task = queue.get(block=False)
                logging.info(f'Выбрана задача с id {self.current_task.id}')
                self.current_task.activate()
                self.current_task.run()
                break
              except Empty:
                pass
          else:
            for task in self.sleeping_tasks:
              if self.current_task.priority < task.priority:
                self.stop_task()
                logging.info(f'Задача с {self.current_task.id} остановлена')
                self.current_task = task
                logging.info(f'Выбрана задача с id {self.current_task.id}')
                self.current_task.release()
                self.current_task.run()
                break
            for priority, queue in self.queues.queues.items():
              if self.current_task.priority < priority:
                try:
                  next_task = queue.get(block=False)
                  self.stop_task()
                  logging.info(f'Задача с {self.current_task.id} остановлена')
                  self.current_task = next_task
                  logging.info(f'Выбрана задача с id {self.current_task.id}')
                  self.current_task.activate()
                  self.current_task.run()
                  break
                except Empty:
                  pass
          time.sleep(0.1)
      except Exception as ex:
        print(ex)

    def stop_task(self):
        if type(self.current_task) == GeneralTask:
            self.current_task.preempt()
            self.queues.put_task(self.current_task)
        if type(self.current_task) == ExtendedTask:
            self.current_task.wait()
            self.sleeping_tasks.add(self.current_task)
