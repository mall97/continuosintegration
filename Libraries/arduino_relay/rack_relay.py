from pyfirmata import Arduino
import time

board = Arduino('COM8')

def arduino_on():
    board.digital[3].write(1)
    time.sleep(10)
    board.digital[3].write(0)

def arduino_off():
    board.digital[3].write(0)

arduino_on()