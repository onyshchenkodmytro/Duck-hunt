import time
from game.timer import Timer
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
def test_timer_counts_down():
    timer = Timer(1)
    time.sleep(1.1)
    assert timer.is_time_up()

def test_timer_reset():
    timer = Timer(5)
    time.sleep(1)
    timer.reset()
    assert timer.get_time_left() > 4.5
