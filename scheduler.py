import logging
import time
from collections import deque
from queue import Empty, Queue
from threading import Thread
from typing import Set, Dict

from task import BaseState, ExtendedState
from task import ExtendedTask, GeneralTask


class Scheduler():
  def __init__(self, events: Queue[ExtendedTask|GeneralTask], dequeue_size=10):
    self.events = events
    self.current_task = None
    self.tasks= {
      3: deque([], dequeue_size),
      2: deque([], dequeue_size),
      1: deque([], dequeue_size),
      0: deque([], dequeue_size)
    }
    self.sleeping_tasks: Set[ExtendedTask] = set()

    sleeping_tasks: Set[ExtendedTask]
    current_task: None|GeneralTask|ExtendedTask
    events: Queue
  def clear(self):
      self.current_task = None


  def pick_task(self):
    self.run_thread()
    try:
      while True:
        if self.current_task and ((type(self.current_task) == GeneralTask and self.current_task.state!=BaseState.RUNNING) or (type(self.current_task) == ExtendedTask and self.current_task.state!=ExtendedState.RUNNING)):
          logging.info(f"Убрана из выполнения задача {self.current_task.id}")
          self.current_task = None
        toRemove= set()
        for task in self.sleeping_tasks:
          if task.activated:
            logging.info(f"Восстановлена задача {task.id}")
            toRemove.add(task)
            self.tasks[task.priority].append(task)
        self.sleeping_tasks -= toRemove
        if self.current_task is None:
          for deque in self.tasks.values():
            try:
              self.current_task = deque.pop()
              logging.info(f'Выбрана задача с id {self.current_task.id}')
              self.current_task.run()
              break
            except IndexError:
              pass
        else:
          for priority,deque in self.tasks.items():
              try:
                if priority > self.current_task.priority:
                  next_task = deque.pop()
                  self.stop_task()
                  logging.info(f'Задача с {self.current_task.id} остановлена')
                  self.current_task = next_task
                  logging.info(f'Выбрана задача с id {self.current_task.id}')
                  self.current_task.run()
                break
              except IndexError:
                pass
        time.sleep(0.1)
    except Exception as ex:
      print(ex)

  def stop_task(self):
      if type(self.current_task) == GeneralTask:
          self.current_task.preempt()
          self.tasks[self.current_task.priority].appendleft(self.current_task)
      if type(self.current_task) == ExtendedTask:
          self.current_task.start_waiting()
          self.sleeping_tasks.add(self.current_task)

  def get_next_task_from_queues(self,queues: Dict[int,Queue]) -> bool:
    for queue in queues.values():
      try:
        self.current_task = queue.get(block=False)
        logging.info(f'Выбрана задача с id {self.current_task.id}')
        self.current_task.run()
        return True
      except Empty:
        return False

  def replace_task_from_queues(self,queues: Dict[int,Queue]) -> bool:
    for priority,queue in queues.items():
      if self.current_task.priority < priority:
        try:
          next_task = queue.get(block=False)
          self.stop_task()
          logging.info(f'Задача с {self.current_task.id} остановлена')
          self.current_task = next_task
          logging.info(f'Выбрана задача с id {self.current_task.id}')
          self.current_task.activate()
          self.current_task.run()
          return True
        except Empty:
          return False


  def convert_events_to_deques(self):
    while True:
      element = self.events.get(block=True)
      element.activate()
      self.tasks[element.priority].appendleft(element)
  def run_thread(self):
    Thread(target=self.convert_events_to_deques).start()
