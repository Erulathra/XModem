import logging

import xmodem


# TODO: WARNING THIS FILE IS ONLY FOR TEST PURPOSES!!!
# TODO: ALL USER INTERFACE SHOULD BE IN main.py

def main():
    # configure logger
    logging.basicConfig(level=logging.DEBUG)

    port_name = "/dev/pts/4"
    baudrate = 9600

    serial_port = xmodem.initialize_serial(port_name, baudrate)
    data = xmodem.receive(serial_port, xmodem.CheckSumEnum.crc)
    print("Cała wiadomość: ")
    print(data.decode("utf-8"))
    serial_port.close()


if __name__ == "__main__":
    main()
