# https://towardsdatascience.com/sensing-the-air-quality-5ed5320f7a56
from sds011 import SDS011  # py-sds011
import aqi  # python-aqi
import time

def active_mode():
    # Start in reporting mode : active
    sensor = SDS011("/dev/ttyUSB0")
    sensor.set_work_period(work_time=1)  # work_time in minutes

    print('waking sensor')
    sensor.sleep(sleep=False)
    print('waiting 10 seconds')
    time.sleep(10)
    print('running sensor query')
    pm25, pm10 = sensor.query()
    print(f"    PMT2.5: {pm25} μg/m3    PMT10 : {pm10} μg/m3")
    print('sleeping sensor')
    sensor.sleep(sleep=True)
    print('waiting 2 seconds')
    time.sleep(2)
    print(sensor)
