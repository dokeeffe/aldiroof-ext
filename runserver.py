import pyfirmata
from bottle import route, run, abort, template, get, post
from pyfirmata import Arduino, util
import time

class FirmataRoofController():

    NAME = "FirmataRoofController"

    def __init__(self, port):
        print('connecting')
        self.board = Arduino(port)
        self.it = util.Iterator(self.board)
        self.it.start()
        self.board.add_cmd_handler(
            pyfirmata.pyfirmata.STRING_DATA, self._messageHandler)
        self.state = 'UNKNOWN'

    def disconnect(self):
        self.board.exit()

    def _messageHandler(self, *args, **kwargs):
        message_string = util.two_byte_iter_to_str(args)
        self.state=message_string

    def update(self):
        super(Collector, self).update()

    def send_arduino_command(self, cmd=[]):
        data = util.str_to_two_byte_iter(cmd + "\0")
        self.board.send_sysex(pyfirmata.pyfirmata.STRING_DATA, data)
        time.sleep(0.2)

    def dispose(self):
        super(Collector, self).dispose()
        try:
            self.board.exit()
        except AttributeError:
            print('exit() raised an AttributeError unexpectedly!')


@route('/')
def index():
    return template('index_template')

@get('/roof')
def roof():
    roof_board.send_arduino_command('QUERY')
    return _roof_state()

@post('/open')
def open():
    roof_board.send_arduino_command('OPEN')
    return _roof_state()

@post('/close')
def close():
    roof_board.send_arduino_command('CLOSE')
    return _roof_state()

@post('/abort')
def abort():
    roof_board.send_arduino_command('ABORT')
    return _roof_state()


def _roof_state():
    return {'state': roof_board.state}

roof_board = FirmataRoofController('/dev/ttyACM0')
run(host='0.0.0.0', port=8080)
