import uos
import machine
import utime

# Credit to https://helloraspberrypi.blogspot.com/2021/02/raspberry-pi-picomicropython-pair-hc-05.html for HC-06/05 guide

# Raspberry Pi Pico/MicroPython
# Pair HC-06 connected to UART0

# default UART
# UART(0, baudrate=9600, bits=8, parity=None, stop=1, tx=0, rx=1)

# Connection:
# RPi Pico UART0  | HC-06
# -----------------------
# GP0(pin 1)      | RX
# GP1(pin 2)      | TX


print(uos.uname())  # Print pico system info
# Initialise new UART instance with a baudrate of 9600 to match the HC-06 default
uart0 = machine.UART(0, baudrate=9600)


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
            resp = uart.readline()
    return str(resp.rstrip(), 'utf8')


# Onboard LED, currently used for feedback that the program has begun running
led_onboard = machine.Pin(25, machine.Pin.OUT)
# LED to toggle when receiving the correct command via bluetooth
led_green = machine.Pin(15, machine.Pin.OUT)

# indicate program started visually
led_onboard.value(0)     # onboard LED OFF/ON for 0.5/1.0 sec
utime.sleep(0.5)
led_onboard.value(1)
utime.sleep(1.0)
led_onboard.value(0)

print(uart0)  # Print UART details for the bluetooth connection
print("Starting Bluetooth...")

while True:
    response = waitResp()  # Await command from bluetooth with 2s timeout

    if response:
        print(response)
        if response == '1':  # If char 1 is sent, turn on LED
            print("Setting LED on")
            led_green.high()
        elif response == '0':  # If char 0 is sent, turn off LED
            print("Setting LED off")
            led_green.low()
        else:
            # Handle unrecognised inputs other than 1 and 0
            print("Error: unrecognised input")
