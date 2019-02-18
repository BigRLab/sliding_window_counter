"""
Thank you for viewing my submission!  Included in my SlidingWindowCounter
are comments and explanations of my implementation.  Please test this class
by using `python test_model.py`.
"""
from datetime import datetime
import bisect


class SlidingWindowCounter:

    time_resolution = 'nanoseconds'
    
    def __init__(self, max_memory_in_seconds=60*60):
        """
        Class instances can be used to track how many events have taken place.  Each 
        instance reports on events that occured within its max_memory_in_seconds.  Register
        events using instance.increment().  This class can handle instance.increment() calls
        down to the nanosecond resolution.  Since each event is stored as an integer in an
        list, this program is supectible to the memory limits of whichever machine/server its
        deployed on.

        Internally, self.events is a sorted list of integers where each entry represents
        an event that occured.  Events are recorded as integers of the number of nanoseconds
        since the class instance was created.  Using integers of nanoseconds instead of floats
        of seconds keeps memory cost lower.  Likewise, keeping track of the unit of time since
        the class was created rather than epoch time of each event keeps the entries in self.events
        small.  
        """
        self.creation_time = self._get_current_time()
        self.max_memory_in_seconds = max_memory_in_seconds
        self.events = []


    def _get_current_time(self):
        """
        Returns epoch time in microseconds as an int.
        """
        return int(datetime.now().timestamp()*1000000)


    def _purge_old_events(self, now):
        """
        Purges timestamps from self.events that are older than max memory.
        """
        if len(self.events) != 0:
            purge_time = now - self.creation_time - self.max_memory_in_seconds*1000000
            if purge_time > 0 and self.events[0] < purge_time:
                del self.events[:bisect.bisect(self.events, purge_time)]


    def increment(self):
        now = self._get_current_time()
        event_time = now - self.creation_time
        if len(self.events) != 0:
            if self.events[-1] == event_time:
                raise ValueError('Failed to increment in SlidingWindowCounter because an event with that timestamp has already been registered.  The supported resolution is {}.'.format(SlidingWindowCounter.time_resolution))
        self.events.append(event_time)


    def _get_events_from_window(self, window_size_in_seconds):
        """
        Takes advantage of the sorted nature of self.events to perform a binary search
        to find the index in self.events where the time window in question starts to
        apply.  That index and the length of the entire list tell us how many events
        are elligable to be counted.

        I used Pythons built in library to do binary search, bisect, because it compiles
        in cpython and is more robustly tested.
        """
        now = self._get_current_time()
        self._purge_old_events(now)
        if len(self.events) == 0:
            return 0
        else:
            lower_window_range = now - self.creation_time - window_size_in_seconds*1000000
            # TODO: Add 2 checks here: If self.events[0] is older than lower_window_range, than return len(self.events).  If self.events[-1] is younger than lower_window_range, return 0.
            return len(self.events) - bisect.bisect(self.events, lower_window_range)

    def num_last_second(self):
        return self._get_events_from_window(1)

    def num_last_minute(self):
        return self._get_events_from_window(60)

    def num_last_hour(self):
        return self._get_events_from_window(3600)
