import time


class Timer:
    def __init__(self, duration):
        self.duration = duration
        self.start_time = time.time()

    def reset(self):
        self.start_time = time.time()

    def is_time_up(self):
        return (time.time() - self.start_time) > self.duration

    def get_time_left(self):
        return max(0, self.duration - (time.time() - self.start_time))
