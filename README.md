# Usage

* Install the `monitor_air_quality` python package
  * This is best done in a `virtualenv` or with `pip install --user monitor_air_quality`
* Create a `config.yaml`
* Run the `monitor_air_quality` script in the same directory as `config.yaml`

This assumes you have an API to submit data to.

## Example output

```
waking sensor
waiting 30 seconds
running sensor query
sleeping sensor
{
    "key": "REDACTED",
    "dt": "2020-09-11T18:36:35.312997",
    "indoor": {
        "pm25": "8.2",
        "pm10": "11.2",
        "aqipm25": "34",
        "aqipm10": "10"
    },
    "outdoor": {
        "pm2_5_atm": "178.99",
        "pm10_0_atm": "209.32",
        "LastSeen": 1599874500,
        "humidity": "47",
        "temp_f": "79",
        "pressure": "1014.95",
        "aqipm2_5_atm": "229",
        "aqipm10_0_atm": "128"
    }
}
result of POST : true
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

