from task import GeneralTask, ExtendedTask
from random import choice, randint

class Generator():
    def __init__(self):
        pass

    def generate(self) -> GeneralTask:
        is_extended = choice([True, False])
        priority = randint(0, 3)
        finish_time = randint(10,100)
        task = ExtendedTask(priority, finish_time) if is_extended else GeneralTask(priority,finish_time)
        print(f'Type  {type(task)}, priority  {task.priority}, id {task.id}')
        return task


generator = Generator()
generator.generate()

