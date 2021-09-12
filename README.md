# Installation

* Install the `monitor_air_quality` python package
  * This is best done in a `virtualenv` or with `pip install --user monitor_air_quality`
* Create a `~/.config/monitor_air_quality_config.yaml` file with config settings
  * See [`monitor_air_quality/monitor_air_quality_config.example.yaml`](monitor_air_quality/monitor_air_quality_config.example.yaml)
* Run `monitor_air_quality --help` to see the options

# Usage

```
usage: monitor_air_quality.py [-h] [--fetch-local-aqi LOCATION]
                              [--fetch-notion-temperature LOCATION]
                              [--notion-sensor SENSOR_NAME]
                              [--fetch-purpleair-data LOCATION]
                              [--command COMMAND]
                              [--alert LOCATION,METRIC,THRESHOLD]
                              [--alert-on-temperature-inversion LOCATION,LOCATION]
                              [--output {print,debug,info,post}]

Gather and post or print air quality and temperature data

optional arguments:
  -h, --help            show this help message and exit
  --fetch-local-aqi LOCATION
                        the local location to use when fetching local data
  --fetch-notion-temperature LOCATION
                        the location to use when fetching the notion API for
                        temperature data
  --notion-sensor SENSOR_NAME
                        the notion sensor name to fetch from
  --fetch-purpleair-data LOCATION
                        the location to use when fetching purpleair data
  --command COMMAND     command to run to fetch remote data
  --alert LOCATION,METRIC,THRESHOLD
                        comma delimited string of location,metric,threshold
  --alert-on-temperature-inversion LOCATION,LOCATION
                        comma delimited string of indoor,outdoor location
                        names
  --output {print,debug,info,post}
                        whether to print or post the results or give debug or
                        info output (default: print)

Examples:
    --command "ssh pi@203.0.113.20 'monitor_air_quality --fetch-local-aqi upstairs'"
    --fetch-local-aqi basement --alert basement,pm25,12
    --notion-sensor "Upstairs hall Sensor" --fetch-notion-temperature upstairs
    --fetch-purpleair-data outdoor
    --alert-on-temperature-inversion upstairs,outdoor --notion-sensor "Upstairs hall Sensor" --fetch-notion-temperature upstairs --fetch-purpleair-data outdoor
    --fetch-local-aqi basement --notion-sensor "Upstairs hall Sensor" --fetch-notion-temperature upstairs --fetch-purpleair-data outdoor --command "ssh -i /home/gene/Documents/monitor_air_quality/id_rsa pi@192.168.0.31 true" --alert upstairs,pm25,12 --alert-on-temperature-inversion upstairs,outdoor
```

# Example outputs

## Output `print`

```
{
    "dt": "2021-09-12T13:25:26.460173",
    "upstairs": {
        "pm25": "4.2",
        "pm10": "7.7",
        "aqipm25": "18",
        "aqipm10": "6",
        "temp_f": "69.99"
    },
    "basement": {
        "pm25": "4.0",
        "pm10": "9.7",
        "aqipm25": "17",
        "aqipm10": "8"
    },
    "outdoor": {
        "pm25": "11.96",
        "pm10": "13.56",
        "LastSeen": 1631478276,
        "humidity": "39",
        "temp_f": "72.57",
        "pressure": "1014.62",
        "aqipm25": "50",
        "aqipm10": "12"
    }
}
```

## Output `post` or `info`

```
INFO:root:Command executed : ssh pi@203.0.113.20 monitor_air_quality : {'dt': '2021-09-12T13:28:27.219094', 'upstairs': {'pm25': '3.7', 'pm10': '6.4', 'aqipm25': '15', 'aqipm10': '6'}}
INFO:root:Local air quality data fetched {'pm25': '4.0', 'pm10': '8.6', 'aqipm25': '17', 'aqipm10': '7'}
INFO:root:Notion temperature data fetched : 69.99
INFO:root:Purpleair data fetched {'pm25': '11.57', 'pm10': '12.63', 'LastSeen': 1631478516, 'humidity': '39', 'temp_f': '73.57', 'pressure': '1014.6', 'aqipm25': '48', 'aqipm10': '11'}
INFO:root:Metric upstairs pm25 3.7 continues to not exceed 12. No transition occurred
INFO:root:It continues to be warmer outside 73.57 than inside 69.99. No transition occurred
```

# Notes

I ended up using the `py-sds011` library instead of the `sds011` library
or just interacting with the serial device directly as it seemed to work
the best for me.

I also chose to use "query mode" instead of "active mode" for the sds011
sensor, though I'm not entirely sure I understand the difference.

Sampling for 30 seconds every 5 minutes would use up 800 of the 1000 hour life
of the sensor in 1 year. I will likely drop this down to 30 seconds every 10
minutes or more.

I read somewhere that the manufacturer recommends a 30 second sample but don't
know where that's written.

