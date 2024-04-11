from generator import Generator
from scheduler import Scheduler
from fifo import Fifo
import logging

logging.basicConfig(level=logging.INFO, filename="test_log.log",filemode="w",encoding="utf-8",format="%(asctime)s %(levelname)s %(message)s")


if __name__=="__main__":
  main_fifo = Fifo(10)
  main_generator = Generator(main_fifo)
  main_scheduler = Scheduler(main_fifo)
  main_generator.run()
  main_scheduler.pick_task()

