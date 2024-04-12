import time
from queue import Queue

import pytest

from generator import Generator
from scheduler import MyDeque
from task import GeneralTask, ExtendedTask, BaseState, ExtendedState

general_task = GeneralTask(1, 2)
extended_task = ExtendedTask(2, 2)


def correct_task(task: GeneralTask | ExtendedTask) -> bool:
  if int(task.id) not in range(1001):
    print(int(task.id))
    return False
  if task.state!=BaseState.SUSPENDED and task.state!=ExtendedState.SUSPENDED:
    print(task.state)
    return False
  if task.priority not in range(4):
    print(task.priority)
    return False
  return True


class Test:
    def test_initial_state(self):
        assert general_task.state == BaseState.SUSPENDED
        assert extended_task.state == ExtendedState.SUSPENDED

    def test_activate(self):
        general_task.activate()
        extended_task.activate()
        assert general_task.state == BaseState.READY
        assert extended_task.state == ExtendedState.READY

    def test_start(self):
        general_task.start()
        extended_task.start()
        assert general_task.state == BaseState.RUNNING
        assert extended_task.state == ExtendedState.RUNNING

    def test_preempt(self):
        general_task.preempt()
        extended_task.preempt()
        assert general_task.state == BaseState.READY
        assert extended_task.state == ExtendedState.READY

    def test_terminate(self):
        general_task.start()
        extended_task.start()
        general_task.terminate()
        extended_task.terminate()
        assert general_task.state == BaseState.SUSPENDED
        assert extended_task.state == ExtendedState.SUSPENDED

    def test_wait(self):
        extended_task.activate()
        extended_task.start()
        extended_task.wait()
        assert extended_task.state == ExtendedState.WAITING

    def test_release(self):
        extended_task.release()
        assert extended_task.state == ExtendedState.READY

    def test_priority(self):
        with pytest.raises(ValueError):
            test_task = GeneralTask(4, 4)
            test_task2 = GeneralTask(-1, -1)
            test_task = ExtendedTask(4, 4)
            test_task2 = ExtendedTask(-1, -1)


    def test_deque_overloading(self):
      deque_var = MyDeque([],10)
      for i in range(11):
        deque_var.append(i)
      assert len(deque_var)==10
      assert not 10 in deque_var
      deque_var = MyDeque([], 10)
      for i in range(11):
        deque_var.appendleft(i)
      assert len(deque_var) == 10
      assert not 10 in deque_var


    def test_generator(self):
      events_loop: Queue[GeneralTask|ExtendedTask] = Queue()
      main_generator = Generator(events_loop)
      main_generator.generate(10)
      for i in range(10):
        task = events_loop.get(block=True)
        assert correct_task(task)




    def test_task_running(self):
      test_task = GeneralTask(3,5)
      test_task.activate()
      test_task.run()
      assert test_task.state == BaseState.RUNNING
      time.sleep(2.1)
      test_task.preempt()
      time.sleep(0.1)
      assert test_task.state == BaseState.READY
      test_task.run()
      time.sleep(3.1)
      assert test_task.state == BaseState.SUSPENDED


    def test_extended_task_running(self):
      test_task = ExtendedTask(3,7)
      test_task.activate()
      test_task.run()
      assert test_task.state == ExtendedState.RUNNING
      time.sleep(2.1)
      test_task.preempt()
      time.sleep(0.1)
      assert test_task.state == ExtendedState.READY
      test_task.run()
      time.sleep(3.1)
      test_task.wait()
      assert test_task.state == ExtendedState.WAITING
      test_task.release()
      test_task.run()
      time.sleep(3.1)
      assert test_task.state == ExtendedState.SUSPENDED

    def test_waiting(self):
      test_task = ExtendedTask(3, 7)
      test_task.activate()
      test_task.start()
      test_task.start_waiting()
      time.sleep(0.1)
      assert test_task.state == ExtendedState.WAITING
      time.sleep(5)
      assert test_task.state == ExtendedState.READY
      assert test_task.activated

