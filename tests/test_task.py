import copy

from generator import Generator
from task import GeneralTask, BaseState, ExtendedTask, ExtendedState


def test_suspended_extended_state(task: ExtendedTask):
  assert task.state == ExtendedState.SUSPENDED
  oldTask = copy.deepcopy(task)
  task.release()
  assert oldTask == task
  task.wait()
  assert oldTask == task
  task.start()
  assert oldTask == task
  task.preempt()
  assert oldTask == task
  task.terminate()
  assert oldTask == task
  task.activate()
  assert task.state == ExtendedState.READY
  taskArguments = getArgumentsExceptState(task)
  oldTaskArguments = getArgumentsExceptState(oldTask)
  assert taskArguments == oldTaskArguments


def test_ready_extended_state(task: ExtendedTask):
  assert task.state == ExtendedState.READY
  oldTask = copy.deepcopy(task)
  task.release()
  assert oldTask == task
  task.wait()
  assert oldTask == task
  task.activate()
  assert oldTask == task
  task.preempt()
  assert oldTask == task
  task.terminate()
  assert oldTask == task
  task.start()
  assert task.state == ExtendedState.RUNNING
  taskArguments = getArgumentsExceptState(task)
  oldTaskArguments = getArgumentsExceptState(oldTask)
  taskArguments.pop("start_time")
  assert taskArguments == oldTaskArguments


def test_running_extended_state(task: ExtendedTask):
  assert task.state == ExtendedState.RUNNING
  oldTask = copy.deepcopy(task)
  task.release()
  assert oldTask == task
  task.activate()
  assert oldTask == task
  task.start()
  assert oldTask == task
  task.preempt()
  assert task.state == ExtendedState.READY
  taskArguments = getArgumentsExceptState(task)
  oldTaskArguments = getArgumentsExceptState(oldTask)
  assert taskArguments == oldTaskArguments
  task.start()
  task.terminate()
  assert task.state == ExtendedState.SUSPENDED
  taskArguments = getArgumentsExceptState(task)
  oldTaskArguments = getArgumentsExceptState(oldTask)
  assert taskArguments == oldTaskArguments
  task.activate()
  task.start()
  task.wait()
  assert task.state == ExtendedState.WAITING
  taskArguments = getArgumentsExceptState(task)
  oldTaskArguments = getArgumentsExceptState(oldTask)
  taskArguments.pop("current_time")
  taskArguments.pop("time_left")
  assert taskArguments == oldTaskArguments


def test_waiting_extended_state(task: ExtendedTask):
  assert task.state == ExtendedState.WAITING
  oldTask = copy.deepcopy(task)
  task.wait()
  assert task == oldTask
  task.start()
  assert task == oldTask
  task.activate()
  assert task == oldTask
  task.terminate()
  assert task == oldTask
  task.preempt()
  assert task == oldTask
  task.release()
  assert task.state == ExtendedState.READY
  taskArguments = getArgumentsExceptState(task)
  oldTaskArguments = getArgumentsExceptState(oldTask)
  assert taskArguments == oldTaskArguments


def test_suspended_general_state(task: GeneralTask):
  assert task.state == BaseState.SUSPENDED
  oldTask = copy.deepcopy(task)
  task.start()
  assert oldTask == task
  task.preempt()
  assert oldTask == task
  task.terminate()
  assert oldTask == task
  task.activate()
  assert task.state == BaseState.READY
  taskArguments = getArgumentsExceptState(task)
  oldTaskArguments = getArgumentsExceptState(oldTask)
  assert taskArguments == oldTaskArguments


def test_ready_general_state(task: GeneralTask):
  assert task.state == BaseState.READY
  oldTask = copy.deepcopy(task)
  task.activate()
  assert oldTask == task
  task.preempt()
  assert oldTask == task
  task.terminate()
  assert oldTask == task
  task.start()
  assert task.state == BaseState.RUNNING
  taskArguments = getArgumentsExceptState(task)
  oldTaskArguments = getArgumentsExceptState(oldTask)
  taskArguments.pop("start_time")
  assert taskArguments == oldTaskArguments


def test_running_general_state(task: GeneralTask):
  assert task.state == BaseState.RUNNING
  oldTask = copy.deepcopy(task)
  task.activate()
  assert oldTask == task
  task.start()
  assert oldTask == task
  task.preempt()
  assert task.state == BaseState.READY
  taskArguments = getArgumentsExceptState(task)
  oldTaskArguments = getArgumentsExceptState(oldTask)
  assert taskArguments == oldTaskArguments
  task.start()
  task.terminate()
  assert task.state == BaseState.SUSPENDED
  taskArguments = getArgumentsExceptState(task)
  oldTaskArguments = getArgumentsExceptState(oldTask)
  assert taskArguments == oldTaskArguments


def getArgumentsExceptState(task: GeneralTask) -> dict:
  taskArguments = copy.deepcopy(vars(task))
  taskArguments.pop("state")
  return taskArguments


def test_general_task(task: GeneralTask):
  test_suspended_general_state(task)
  test_ready_general_state(task)
  test_running_general_state(task)


def test_extended_task(task: ExtendedTask):
  test_suspended_extended_state(task)
  test_ready_extended_state(task)
  test_running_extended_state(task)
  test_waiting_extended_state(task)


def test_tasks():
  taskTypes = set()
  while True:
    task = Generator().generate()
    if type(task) is GeneralTask:
      test_general_task(task)
    elif type(task) is ExtendedTask:
      test_extended_task(task)
    taskTypes.add(type(task))
    if len(taskTypes) == 2:
      break
