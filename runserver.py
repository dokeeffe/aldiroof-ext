import pyfirmata
from bottle import route, run, abort, template, get, post
from pyfirmata import Arduino, util
import time
import requests

class FirmataRoofController():

    NAME = "FirmataRoofController"

    def __init__(self, port):
        print('connecting')
        self.board = Arduino(port)
        self.board.add_cmd_handler(
            pyfirmata.pyfirmata.STRING_DATA, self._messageHandler)
        self.roofstate = 'UNKNOWN'
        self.shutterstate = 'UNKNOWN'

    def disconnect(self):
        self.board.exit()

    def _messageHandler(self, *args, **kwargs):
        message_string = util.two_byte_iter_to_str(args)
        if 'SHUTTER' in message_string:
            self.shutterstate = message_string
        else:
            self.roofstate=message_string

    def update(self):
        super(Collector, self).update()

    def send_arduino_command(self, cmd=[]):
        self.it = util.Iterator(self.board)
        self.it.start()
        data = util.str_to_two_byte_iter(cmd + "\0")
        self.board.send_sysex(pyfirmata.pyfirmata.STRING_DATA, data)
        time.sleep(0.2)
        self.it.board = None

    def dispose(self):
        super(Collector, self).dispose()
        try:
            self.board.exit()
        except AttributeError:
            print('exit() raised an AttributeError unexpectedly!')

def is_safe_to_open():
    try:
        resp = requests.get('http://192.168.1.227:8080/weather/current')
        if resp.json().get('rain') == False:
            return True
        return False
    except:
        return False

@route('/')
def index():
    return template('index_template')

@get('/roof')
def roof():
    roof_board.send_arduino_command('QUERY')
    return _roof_state()

@get('/shutter')
def shutter():
    roof_board.send_arduino_command('SHUTTERQUERY')
    return _shutter_state()

@get('/safe')
def safe():
    return {'safe': is_safe_to_open()}

@post('/open')
def open():
    if is_safe_to_open():
        roof_board.send_arduino_command('OPEN')
        return _roof_state()
    else:
        return abort(400, 'Not safe to open roof now')

@post('/shutteropen')
def openshutter():
    if is_safe_to_open():
        roof_board.send_arduino_command('SHUTTEROPEN')
        return _shutter_state()
    else:
        return abort(400, 'Not safe to open shutter now')

@post('/close')
def close():
    roof_board.send_arduino_command('CLOSE')
    return _roof_state()

@post('/shutterclose')
def closeshutter():
    roof_board.send_arduino_command('SHUTTERCLOSE')
    return _shutter_state()


@post('/abort')
def abort():
    roof_board.send_arduino_command('ABORT')
    return _roof_state()


def _roof_state():
    return {'state': roof_board.roofstate}

def _shutter_state():
    return {'state': roof_board.shutterstate}

roof_board = FirmataRoofController('/dev/ttyACM0')
run(host='0.0.0.0', port=8080)

