from queue import Queue

from generator import Generator
from scheduler import Scheduler
import logging

logging.basicConfig(level=logging.INFO, filename="test_log.log",filemode="w",encoding="utf-8",format="%(asctime)s %(levelname)s %(message)s")


if __name__=="__main__":
  events_loop=Queue()
  main_generator = Generator(events_loop)
  main_scheduler = Scheduler(events_loop)
  main_generator.run()
  main_scheduler.pick_task()

