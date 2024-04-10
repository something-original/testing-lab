from task import GeneralTask, ExtendedTask
from generator import Generator
from scheduler import Scheduler
from fifo import Fifo
from threading import Thread, Event

if __name__=="__main__":
  main_fifo = Fifo(10)
  main_generator = Generator(main_fifo)
  stop_event = Event()
  main_scheduler = Scheduler(main_fifo, stop_event)
  main_generator.run()
  main_scheduler.pick_task()

