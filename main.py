import uos
import machine
import utime

# Raspberry Pi Pico/MicroPython
# Pair HC-06 connected to UART0

# default UART
# UART(0, baudrate=9600, bits=8, parity=None, stop=1, tx=0, rx=1)

# Connection:
# RPi Pico UART0  HC-06
# GP0(pin 1)      RX
# GP1(pin 2)      TX


# To enter AT-Command mode-

# HC06:
# Power-up in NOT CONNECTED

print(uos.uname())
uart0 = machine.UART(0, baudrate=9600)  # at-command

# 2 sec timeout is arbitrarily chosen


def sendCMD_waitResp(cmd, uart=uart0, timeout=2000):
    print("CMD: " + cmd)
    uart.write(cmd)
    waitResp(uart, timeout)
    print()


def waitResp(uart=uart0, timeout=2000):
    prvMills = utime.ticks_ms()
    resp = b""
    while (utime.ticks_ms()-prvMills) < timeout:
        if uart.any():
            resp = b"".join([resp, uart.read(1)])
    return str(resp, 'utf-8')


led_onboard = machine.Pin(25, machine.Pin.OUT)
led_green = machine.Pin(15, machine.Pin.OUT)

# indicate program started visually
led_onboard.value(0)     # onboard LED OFF/ON for 0.5/1.0 sec
utime.sleep(0.5)
led_onboard.value(1)
utime.sleep(1.0)
led_onboard.value(0)

print(uart0)
print("Starting Bluetooth...")

while True:
    response = waitResp()

    if response:
        print(response)
        if response == '1':
            print("Setting LED on")
            led_green.high()
        elif response == '0':
            print("Setting LED off")
            led_green.low()
        else:
            print("Error: unrecognised input")
