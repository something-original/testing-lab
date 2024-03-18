import re

import pytest

from generator import Generator
from task import GeneralTask, BaseState, ExtendedTask, ExtendedState


def test_generator():
  tasksTypes = set()
  tasksPriorities = set()
  while True:
    task = Generator().generate()
    isCorrect = isCorrectTask(task)
    assert isCorrect
    if not isCorrect:
      print("Failed: incorrect task generated")
      break
    tasksTypes.add(task.__class__)
    tasksPriorities.add(task.priority)
    if (len(tasksTypes) == 2) & (len(tasksPriorities) == 4):
      break

def isCorrectTask(task: GeneralTask) -> bool:
  pattern = re.compile("\d{4}")
  return (task.priority in range(4)) & bool(pattern.fullmatch(task.id)) & (task.finish_time > 0) & isCorrectStartState(task)

def isCorrectStartState(task: GeneralTask) -> bool:
  if type(task) is GeneralTask:
    return task.state == BaseState.SUSPENDED
  elif type(task) is ExtendedTask:
    return task.state == ExtendedState.SUSPENDED
  return False
