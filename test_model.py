"""
Runs unit tests for the SlidingWindowCounter found in model.py. To run
type `python test_model.py`.  Tests take under 4 seconds.
"""
import time

from model import SlidingWindowCounter

def test_zero_events():
    counter = SlidingWindowCounter()
    assert counter.num_last_second() == 0
    assert counter.num_last_minute() == 0
    assert counter.num_last_hour() == 0

def test_one_event():
    counter = SlidingWindowCounter()
    counter.increment()
    assert counter.num_last_second() == 1
    assert counter.num_last_minute() == 1
    assert counter.num_last_hour() == 1

def test_expired_event():
    counter = SlidingWindowCounter()
    counter.increment()
    time.sleep(1)
    counter.increment()
    assert counter.num_last_second() == 1
    assert counter.num_last_minute() == 2
    assert counter.num_last_hour() == 2

def test_max_memory():
    counter = SlidingWindowCounter(max_memory_in_seconds=1)
    # The following increment call should be forgotten because of a sleep later on.
    counter.increment()
    assert counter.num_last_second() == 1
    assert counter.num_last_minute() == 1
    assert counter.num_last_hour() == 1
    time.sleep(2)
    assert counter.num_last_second() == 0
    assert counter.num_last_minute() == 0
    assert counter.num_last_hour() == 0
    counter.increment()
    assert counter.num_last_second() == 1
    assert counter.num_last_minute() == 1
    assert counter.num_last_hour() == 1

if __name__ == '__main__':
    test_zero_events()
    test_one_event()
    test_expired_event()
    test_max_memory()
    print('Woohoo! All tests passed!')