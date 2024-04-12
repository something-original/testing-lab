import random
import time
from queue import Queue

from generator import Generator
from scheduler import Scheduler
import logging

from task import GeneralTask, ExtendedTask

logging.basicConfig(level=logging.INFO, filename="test_log.log",filemode="w",encoding="utf-8",format="%(asctime)s %(levelname)s %(message)s")


def createRandomTask(priority: int, time_left:int) -> GeneralTask | ExtendedTask:
  is_extended = random.choice([True, False])
  task = ExtendedTask(priority, time_left) if is_extended else GeneralTask(priority, time_left)
  return task


class Test:

  """
  Тестирование выполнения задач в порядке FIFO
  """
  def testFifoSequence(self):
    events_loop = Queue()
    main_scheduler = Scheduler(events_loop)
    main_scheduler.pick_task_threaded()
    priority = random.randint(0,3)
    task1 = createRandomTask(priority, 1)
    events_loop.put(task1)
    time.sleep(0.1)
    task2 = createRandomTask(priority,1)
    events_loop.put(task2)
    time.sleep(0.1)
    task3 = createRandomTask(priority,1)
    events_loop.put(task3)
    time.sleep(0.2)
    assert main_scheduler.current_task == task1
    time.sleep(1.1)
    assert main_scheduler.current_task == task2
    time.sleep(1.1)
    assert main_scheduler.current_task == task3
    time.sleep(1.1)
    assert main_scheduler.current_task is None

  """
    Тестирование того, что при появлении задачи с более высоким приоритетом задача с более низким приоритетом прекращает выполнение
  """
  def testHighPriorityStopsLowPriority(self):
    events_loop=Queue()
    main_scheduler = Scheduler(events_loop,allow_stopping=False)
    main_scheduler.pick_task_threaded()
    task1=createRandomTask(0,2)
    task2=createRandomTask(1,1)
    task3=createRandomTask(1,2)
    task4=createRandomTask(2,2)
    task5=createRandomTask(3,2)
    events_loop.put(task1)
    time.sleep(0.2)
    assert main_scheduler.current_task == task1
    time.sleep(1.1)
    events_loop.put(task2)
    events_loop.put(task3)
    time.sleep(0.2)
    assert main_scheduler.current_task == task2
    time.sleep(1.1)
    assert main_scheduler.current_task == task3
    time.sleep(1.1)
    events_loop.put(task4)
    time.sleep(0.2)
    assert main_scheduler.current_task == task4
    time.sleep(1.1)
    events_loop.put(task5)
    time.sleep(0.2)
    assert main_scheduler.current_task == task5

  """
      Тестирование того, что при появлении задачи с более низким приоритетом задача с более высоким приоритетом не прекращает выполнение
  """
  def testLowPriorityNotStopsHighPriority(self):
    events_loop = Queue()
    main_scheduler = Scheduler(events_loop,allow_stopping=False)
    main_scheduler.pick_task_threaded()
    task1 = createRandomTask(3, 2)
    task2 = createRandomTask(2, 1)
    task3 = createRandomTask(2, 2)
    task4 = createRandomTask(1, 2)
    task5 = createRandomTask(0, 2)
    events_loop.put(task1)
    time.sleep(0.2)
    assert main_scheduler.current_task == task1
    time.sleep(1)
    events_loop.put(task2)
    events_loop.put(task3)
    time.sleep(0.1)
    assert main_scheduler.current_task == task1
    time.sleep(1.1)
    assert main_scheduler.current_task == task2
    time.sleep(1)
    assert main_scheduler.current_task == task3
    time.sleep(1.1)
    events_loop.put(task4)
    time.sleep(0.1)
    assert main_scheduler.current_task == task3
    time.sleep(1)
    assert main_scheduler.current_task == task4
    time.sleep(1.1)
    events_loop.put(task5)
    time.sleep(0.1)
    assert main_scheduler.current_task == task4
    time.sleep(1)
    assert main_scheduler.current_task == task5

  """
    ИЗМЕНИТЬ В task time.sleep ПЕРЕД ТЕСТИРОВАНИЕМ!
    Тестирование Extended. Проверяется, что при появлении задачи с более высоким приоритетом задача с более низким приоритетом переходит в состояние waiting, ждёт некоторое время и встаёт в начало очереди своего приоритета
    """
  def testWaitingImplementedCorrectly(self):
    events_loop = Queue()
    main_scheduler = Scheduler(events_loop, allow_stopping=False)
    main_scheduler.pick_task_threaded()
    task1 = ExtendedTask(0, 2)
    print(task1.id)
    task2 = ExtendedTask(1, 1)
    print(task2.id)
    task3 = ExtendedTask(0, 2)
    events_loop.put(task1)
    time.sleep(0.2)
    print(main_scheduler.current_task.id)
    assert main_scheduler.current_task == task1
    time.sleep(1.1)
    events_loop.put(task3)
    time.sleep(0.2)
    events_loop.put(task2)
    time.sleep(0.2)
    print(main_scheduler.current_task.id)
    assert main_scheduler.current_task == task2
    time.sleep(1.1)
    print(main_scheduler.current_task.id)
    assert main_scheduler.current_task == task1
    time.sleep(1.1)
    print(main_scheduler.current_task.id)
    assert main_scheduler.current_task == task3

  """
  Тестирование GeneralTask. Проверяется, что при появлении задачи с более высоким приоритетом задача с более низким приоритетом прекращает выполнение и встаёт в конец очереди своего приоритета
  """
  def testStoppingImplementedCorrectly(self):
    events_loop = Queue()
    main_scheduler = Scheduler(events_loop, allow_stopping=False)
    main_scheduler.pick_task_threaded()
    task1 = GeneralTask(0, 2)
    task2 = GeneralTask(1, 1)
    task3 = GeneralTask(1, 2)
    task4 = GeneralTask(2, 2)
    task5 = GeneralTask(3, 2)
    task6 = GeneralTask(2, 1)
    events_loop.put(task1)
    time.sleep(0.2)
    assert main_scheduler.current_task == task1
    time.sleep(1.1)
    events_loop.put(task2)
    events_loop.put(task3)
    time.sleep(0.2)
    assert main_scheduler.current_task == task2
    time.sleep(1.1)
    assert main_scheduler.current_task == task3
    time.sleep(1.1)
    events_loop.put(task4)
    time.sleep(0.2)
    assert main_scheduler.current_task == task4
    time.sleep(1.1)
    events_loop.put(task6)
    time.sleep(0.2)
    events_loop.put(task5)
    time.sleep(0.2)
    assert main_scheduler.current_task == task5
    time.sleep(2.1)
    assert main_scheduler.current_task == task6
    time.sleep(1.1)
    assert main_scheduler.current_task == task4
    time.sleep(1.1)
    assert main_scheduler.current_task == task3
    time.sleep(1.1)
    assert main_scheduler.current_task == task1
