from sds011 import SDS011  # sds011
import time

port = "/dev/ttyUSB0"

sds = SDS011(port=port)
time.sleep(1)
print(sds)
time.sleep(1)
sds.sleep()
time.sleep(1)
print(sds)


exit(0)
# sds.set_working_period(rate=5) # one measurment every 5 minutes offers decent granularity and at least a few years of lifetime to the sensor
sds.set_working_period(rate=1)
while True:
    meas = sds.read_measurement()
    print(meas)
