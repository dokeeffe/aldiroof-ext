# aldiroof-ext

Extensions for [indi-aldiroof](https://github.com/dokeeffe/indi-aldiroof) to enable opening and closing roof outside of INDI.

### Why is this needed

This is only useful if you use https://github.com/dokeeffe/indi-aldiroof to control an observatory roof and you want to add an HTTP api to control it.

This exists because indi-aldiroof depends on a USB connection between the arduino relay controller and a 'computer'. Since the distance was too great (>5M), USB became unreliable and this was born to run on a raspberry pi physically next to the arduino relay cotroller.
Provides a simple http interface to open and close the observatory roof over HTTP.


### Installing

* Connect a raspberry pi to the arduino used to conrol the roof from https://github.com/dokeeffe/indi-aldiroof
* Clone this repo on the pi into /home/pi/code
* Create a venv in this repo's dir `python -m venv ./venv`
* install requirements.txt `pip install -r requirements.txt`
* Copy the bottle.service file to `/lib/systemd/system/bottle.service` 
* Run `sudo systemctl daemon-reload`
* Run `sudo systemctl enable bottle.service`
* Reboot and the service should startup `sudo systemctl status bottle.service`
* Control the roof via HTTP (example: Get the roof status `curl http://192.168.1.13:8080/roof`)
