from task import GeneralTask, ExtendedTask, generate_id

print(generate_id())

task1 = GeneralTask(0)
print(task1.priority)
print(task1.state)
task1.activate()
print(task1.state)
task1.start()
print(task1.state)
task1.preempt()
print(task1.state)
task1.start()
print(task1.state)
task1.terminate()
print(task1.state)

try:
    task2 = ExtendedTask(4)
except ValueError:
    pass

task2 = ExtendedTask(3)
print(task2.priority)
print(task2.state)
task2.activate()
print(task2.state)
task2.start()
print(task2.state)
task2.preempt()
print(task2.state)
task2.start()
print(task2.state)
task2.wait()
print(task2.state)
task2.release()
print(task2.state)
task2.start()
print(task2.state)
task2.terminate()
print(task2.state)

