from machine import UART
import time

# Configure the UART connection to the SIM7000G
uart = UART(1, baudrate=9600, tx=17, rx=16)

# Function to send an AT command and print the response
def send_at(command, delay=1000):
    print("Sending command: {}".format(command))
    uart.write(command + "\r\n")
    time.sleep_ms(delay)
    print(uart.read().decode())

# Initialize the SIM7000G
send_at("AT")
send_at("AT+CGATT=1")  # Attach to GPRS
send_at("AT+SAPBR=3,1,\"CONTYPE\",\"GPRS\"")  # Set connection type to GPRS
send_at("AT+SAPBR=3,1,\"APN\",\"internet\"")  # Set APN
send_at("AT+SAPBR=3,1,\"USER\",\"internet\"")  # Set username
send_at("AT+SAPBR=3,1,\"PWD\",\"internet\"")  # Set password
send_at("AT+SAPBR=1,1")  # Open a GPRS context
send_at("AT+SAPBR=2,1")  # Query the GPRS context to confirm connection
