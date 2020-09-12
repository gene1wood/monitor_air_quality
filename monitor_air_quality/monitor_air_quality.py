#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import json
import hashlib
from datetime import datetime
import yaml  # PyYAML
import requests  # requests
from sds011 import SDS011  # py-sds011
import aqi  # python-aqi

# sudo usermod -a -G dialout yourusername
# https://cdn.sparkfun.com/assets/parts/1/2/2/7/5/Laser_Dust_Sensor_Control_Protocol_V1.3.pdf

with open('config.yaml') as f:
    config = yaml.safe_load(f)

HASHED_KEY = hashlib.pbkdf2_hmac(
    'sha256',
    str.encode(config['KEY']),
    str.encode(config['SALT']),
    100000).hex()


def get_outdoor_data():
    # https://docs.google.com/document/d/15ijz94dXJ-YAZLi9iZ_RaBwrZ4KtYeCy08goGBwnbCU/edit
    result = requests.get(f"https://www.purpleair.com/json?key={config['PURPLE_AIR_KEY']}&show={config['PURPLE_AIR_DEVICE_ID']}")
    data = {
        'pm2_5_atm': None,
        'pm10_0_atm': None,
        'LastSeen': None,
        'humidity': None,
        'temp_f': None,
        'pressure': None
    }
    for record in result.json().get('results', []):
        # https://github.com/MazamaScience/AirSensor/blob/master/documents/PurpleAir_CF=ATM_vs_CF=1.md
        for field in data.keys():
            if field in record:
                if data[field] is None:
                    data[field] = record[field]
                else:
                    if field in ['pm2_5_atm', 'pm10_0_atm']:
                        data[field] = "{:.2f}".format(
                            sum([float(data[field]), float(record[field])]) / 2)
                    # We'll assume LastSeen values are similar
    data['aqipm2_5_atm'] = str(aqi.to_iaqi(aqi.POLLUTANT_PM25, str(data['pm2_5_atm'])))
    data['aqipm10_0_atm'] = str(aqi.to_iaqi(aqi.POLLUTANT_PM10, str(data['pm10_0_atm'])))
    return data


# https://towardsdatascience.com/sensing-the-air-quality-5ed5320f7a56
def query_mode():
    # Start in reporting mode : query/home/pi/.local/bin
    sensor = SDS011("/dev/ttyUSB0", use_query_mode=True)
    sensor.set_work_period(work_time=0)  # work_time is continuous
    print('waking sensor')
    sensor.sleep(sleep=False)  # wake sensor
    print('waiting 30 seconds')
    time.sleep(30)  # capture 30 seconds of data
    print('running sensor query')
    pm25, pm10 = sensor.query()
    print('sleeping sensor')
    sensor.sleep()  # sleep sensor
    # print(f"    PMT2.5: {pm25} μg/m3    PMT10 : {pm10} μg/m3")
    data = {
        'key': HASHED_KEY,
        'dt': datetime.now().isoformat(),
        'indoor': {
            'pm25': str(pm25),
            'pm10': str(pm10),
            'aqipm25': str(aqi.to_iaqi(aqi.POLLUTANT_PM25, str(pm25))),
            'aqipm10': str(aqi.to_iaqi(aqi.POLLUTANT_PM10, str(pm10)))
        },
        'outdoor': get_outdoor_data()
    }
    print(json.dumps(data, indent=4))
    result = requests.post(config['URL'], json=data)
    print(f'result of POST : {result.text}')


if __name__ == "__main__":
    query_mode()
