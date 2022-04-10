import check_sum as cs
import serial as ser

import xmodem


def main():
    test = "ziemniaki sa fajne i mozna je wrzucic do stringa, a ja musze zrobic 128 bajtowego stringa wiec mi sie " \
           "przydadza, jeszcze tylko a"

    crc = cs.crc_check_sum(bytes(test, "ascii"))
    print(cs.algebraic_check_sum(bytes(test, "ascii")))
    print(int.from_bytes(crc, 'big'))

    port_name = "/dev/pts/1"
    baudrate = 9600

    serial_one = ser.Serial(port_name, baudrate)
    # serial_one.write("Hi!")

    print(xmodem.prepare_packets(bytes(test, "ascii"), xmodem.CheckSumEnum.CRC))


if __name__ == "__main__":
    main()