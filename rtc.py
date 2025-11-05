# rtc.py — RTC helper with fallback tick timer
from machine import RTC
import time

rtc = RTC()

# Start in "unknown time"
_last_time = [0, 0]  # [epoch_ms, seconds_at_that_time]
_last_update_ms = time.ticks_ms()

def set_time(hh, mm):
    global _last_time, _last_update_ms

    # Fake date — we only care about time
    rtc.datetime((2025,1,1,0, hh, mm, 0, 0))

    _last_time = [time.ticks_ms(), hh*3600 + mm*60]
    _last_update_ms = _last_time[0]

def now():
    global _last_time, _last_update_ms

    t = rtc.datetime()  # (year, month, day, weekday, hour, minute, second, subseconds)
    hh = t[4]
    mm = t[5]

    # If RTC hasn't been set yet, or lost power: fallback timer
    if hh == 0 and mm == 0 and _last_time[1] != 0:
        elapsed = time.ticks_diff(time.ticks_ms(), _last_update_ms) // 1000
        seconds = (_last_time[1] + elapsed) % 86400
        hh = seconds // 3600
        mm = (seconds % 3600) // 60

    return f"{hh:02}:{mm:02}"
