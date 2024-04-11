import logging
import random
import time
from collections import deque
from queue import Empty, Queue
from threading import Thread
from typing import Set, Dict, Deque, Any

from task import BaseState, ExtendedState
from task import ExtendedTask, GeneralTask


class MyDeque(Deque):
  def append(self, __x: Any) -> None:
    if self.__len__() < self.maxlen:
      super().append(__x)

  def appendleft(self, __x: Any) -> None:
    if self.__len__() < self.maxlen:
      super().appendleft(__x)

class Scheduler():
  def __init__(self, events: Queue[ExtendedTask|GeneralTask], dequeue_size=10):
    self.events = events
    self.current_task = None
    self.tasks= {
      3: MyDeque([], dequeue_size),
      2: MyDeque([], dequeue_size),
      1: MyDeque([], dequeue_size),
      0: MyDeque([], dequeue_size)
    }
    self.sleeping_tasks: Set[ExtendedTask] = set()

    tasks: Dict[int,MyDeque[ExtendedTask|GeneralTask]]
    sleeping_tasks: Set[ExtendedTask]
    current_task: None|GeneralTask|ExtendedTask
    events: Queue
  def clear(self):
      self.current_task = None


  def pick_task(self):
    self.run_thread()
    try:
      while True:
        self._clear_stopped_tasks()
        self._recover_waiting_tasks()
        self._kill_top_priority_task()
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

  def _recover_waiting_tasks(self):
    toRemove = set()
    for task in self.sleeping_tasks:
      if task.activated:
        logging.info(f"Восстановлена задача {task.id}")
        toRemove.add(task)
        self.tasks[task.priority].append(task)
    self.sleeping_tasks -= toRemove

  def _clear_stopped_tasks(self):
    if self.current_task and (
      (type(self.current_task) == GeneralTask and self.current_task.state != BaseState.RUNNING) or (
      type(self.current_task) == ExtendedTask and self.current_task.state != ExtendedState.RUNNING)):
      logging.info(f"Убрана из выполнения задача {self.current_task.id}")
      self.current_task = None

  def stop_task(self):
      if type(self.current_task) == GeneralTask:
          self.current_task.preempt()
          self.tasks[self.current_task.priority].appendleft(self.current_task)
      if type(self.current_task) == ExtendedTask:
          self.current_task.start_waiting()
          self.sleeping_tasks.add(self.current_task)

  def convert_events_to_deques(self):
    while True:
      element = self.events.get(block=True)
      element.activate()
      self.tasks[element.priority].appendleft(element)
  def run_thread(self):
    Thread(target=self.convert_events_to_deques).start()

  def _kill_top_priority_task(self):
    if self.current_task and type(self.current_task) == ExtendedTask and self.current_task.priority==3:
      fortune = random.randint(0,10)
      if fortune==0:
        logging.info(f'Задача с {self.current_task.id} остановлена')
        self.stop_task()
        self.current_task=None
