from task import GeneralTask, ExtendedTask, BaseState, ExtendedState
from fifo import Fifo
from queue import Full
import pytest

general_task = GeneralTask(1, 10)
extended_task = ExtendedTask(2, 4)


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

    def test_full_queue(self):
        with pytest.raises(Full):
            test_fifo = Fifo(5)
            for i in range(0, 6):
                test_fifo.receive_task(GeneralTask(1, 1))



