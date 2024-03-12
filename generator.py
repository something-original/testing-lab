from task import GeneralTask, ExtendedTask
from random import choice, randint

class Generator():
    def __init__(self):
        pass
    
    def generate(self):
        is_extended = choice([True, False])
        priority = randint(0, 3)
        task = ExtendedTask(priority) if is_extended else GeneralTask(priority)
        print(f'Type  {type(task)}, priority  {task.priority}, id {task.id}')
        #return task


generator = Generator()
generator.generate()

