# ovh-notifier
[forked from here](https://git.pofilo.fr/pofilo/kimsufi/releases)

Sends an alert when your OVH server is available.

## Requirements

+ **python 3.9**

## Purpose

The objective is to **send notifications** when the OVH server you want is available in the zone(s) desired.
There is (for now) 3 types of notifications:
+ Email
+ HTTP request
+ Telegram message
+ Discord webhook

A notification will be send to the notifiers configured when the server is available and when it's not anymore.

## Documentation

[link to the documentation](https://github.com/Wqntedpw/ovh-notifier/wiki)

## Installation

### Via docker
+ Download the last stable version [available here](https://github.com/Wqntedpw/ovh-notifier/releases)
+ `cp config/kimsufi.sample.conf config/kimsufi.conf`
+ Edit *config/kimsufi.conf*
+ docker-compose up -d

### Manual
+ Download the last stable version [available here](https://github.com/Wqntedpw/ovh-notifier/releases)
+ `cd kimsufi`
+ Create virtual environment: `python3 -m env .`
+ Source it: `source bin/activate`
+ Install dependencies: `pip install -r requirements.txt`
+ `cp config/kimsufi.sample.conf config/kimsufi.conf`
+ Edit *config/kimsufi.conf*
+ `cd src`
+ `python3 kimsufi.py` or `python3 -u kimsufi.py > log.txt &` if you want to use it as a daemon *(the PID is given in the first lines of the logs)*


#### Options

+ `-c`, `--conf`
    + Specify the path of the configuration file (relative to `kimsufi/src` or absolute)
    + Default value is `../config/kimsufi.conf`

### Testing configuration

It would be too bad to not be notified because of a bad configuration.
To test it, in your configuration file, you can change your `API_URL` with `https://github.com/Wqntedpw/ovh-notifier/example-availability-file.json` . In this file, the server `1623hardzone1` is available in the zone `sbg`. If you start the script (`python3 kimsufi.py`), you should receive notifications by the notifiers you configured.

### Adding notifier

You can hack the script and add notifiers in the file `notifications.py`. Simply create a new function (in parameter, you can have the config and the boolean meaning if the server is found or not) and call it into `send_notifications(config, found)`, modify the configuration file if needed, et voilà!

### Linter

`pylint` is a bit used for this project (not yet perfect, feel free to help if you have some time!).

```
pip install pylint
pylint --disable=C0301 src/*\.py
```

*Screen are long enough to print larger lines...*

## License

This project is licensed under the GNU GPL License. See the [LICENSE](LICENSE) file for the full license text.

## Credits

+ [@Pofilo](https://git.pofilo.fr/pofilo/)
+ [@c4s4](https://github.com/c4s4)

## Bugs

If you experience an issue, you have other ideas to the developpement or anything else, feel free to report it or fix it with a PR

