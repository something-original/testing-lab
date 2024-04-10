from task import GeneralTask, ExtendedTask
from generator import Generator
from scheduler import Scheduler
from fifo import Fifo
from threading import Thread, Event

main_fifo = Fifo(10)
main_generator = Generator(main_fifo)
stop_event = Event()
main_scheduler = Scheduler(main_fifo, stop_event)

main_generator.generate(testing_mode=False)

scheduler_thread = Thread(target = main_scheduler.pick_task(), daemon=True, args=(stop_event,))
task_thread = Thread(target = main_scheduler.run_task(), daemon=True, args=(stop_event,))



