from enum import Enum

import serial as ser

import check_sum
from check_sum import algebraic_check_sum, crc_check_sum

SOH = b'\x01'
EOT = b'\x04'
ACK = b'\x06'
NAK = b'\x15'
CAN = b'\x18'
SUB = b'\x1A'
CRC = b'\x43'


class CheckSumEnum(Enum):
    algebraic = NAK
    crc = CRC


class ReceiverDoesNotStartTransferException(Exception):
    pass


class SenderDoesNotAcceptTransferException(Exception):
    pass


class WrongPacketNumberException(Exception):
    pass


class WrongCheckSumException(Exception):
    pass


class WrongHeaderException(Exception):
    pass


class ReceiverSendUnexpectedResponseException(Exception):
    pass


def initialize_serial(port: str, baudrate: int = 9600, timeout=3):
    serial_port = ser.Serial()
    serial_port.baudrate = baudrate
    serial_port.port = port
    serial_port.timeout = timeout
    serial_port.parity = ser.PARITY_NONE
    serial_port.stopbits = ser.STOPBITS_ONE
    serial_port.bytesize = ser.EIGHTBITS
    serial_port.open()
    return serial_port


def send(serial_port: ser.Serial, data: bytes):
    check_sum_type = wait_for_start_sending_and_get_check_sum_type(serial_port)
    packets = prepare_packets(data, check_sum_type)

    packet_number = 0
    while packet_number < len(packets):
        serial_port.write(packets[packet_number])

        # when receiver sends NAK send packer another time
        response = serial_port.read(1)
        if response == ACK:
            packet_number += 1
        elif response == NAK:
            continue
        else:
            raise ReceiverSendUnexpectedResponseException

    response = None
    while response != ACK:
        serial_port.write(EOT)
        response = serial_port.read()


def wait_for_start_sending_and_get_check_sum_type(serial_port: ser.Serial) -> CheckSumEnum:
    for i in range(6):
        message = serial_port.read(1)
        if message == NAK:
            return CheckSumEnum.algebraic
        elif message == CRC:
            return CheckSumEnum.crc

    raise ReceiverDoesNotStartTransferException


def prepare_packets(data: bytes, check_sum_type: CheckSumEnum) -> [bytes]:
    # split data intro 128 bytes long blocks
    blocks = [data[i:i + 128] for i in range(0, len(data), 128)]

    packets = []
    for packet_number in range(len(blocks)):
        packet = bytearray()
        packet += create_header(check_sum_type, packet_number)

        # fill last packet with ^z to make it 128 byte length
        if len(blocks[packet_number]) < 128:
            blocks[packet_number] = fill_block_with_sub(blocks[packet_number])

        # append data block
        packet += bytearray(blocks[packet_number])

        # calculate check sum and append it to packet
        calculated_check_sum = None
        if check_sum_type == CheckSumEnum.algebraic:
            calculated_check_sum = algebraic_check_sum(blocks[packet_number])
        elif check_sum_type == CheckSumEnum.crc:
            calculated_check_sum = crc_check_sum(blocks[packet_number])

        packet += bytearray(calculated_check_sum)

        # append packet to packet list
        packets.append(bytes(packet))

    return packets


def create_header(check_sum_type: CheckSumEnum, packet_number: int) -> bytearray:
    # append checkSumType
    header = bytearray(SOH)

    # packet number starts at 1 when is lower than 255
    packet_number += 1

    # append packet number and it's compliment
    header.append(packet_number % 255)
    header.append(255 - (packet_number % 255))

    return header


def fill_block_with_sub(block: bytes):
    block = bytearray(block)
    for i in range(128 - len(block)):
        block += bytearray(SUB)

    return bytes(block)


def receive(serial_port: ser.Serial, check_sum_type: CheckSumEnum) -> bytes:
    result = bytearray()
    # Wait for sender response
    for i in range(20):
        serial_port.write(check_sum_type.value)
        # read packet
        packet = None


def read_package(serial_port: ser.Serial, check_sum_type: CheckSumEnum):
    if check_sum_type == CheckSumEnum.algebraic:
        packet = serial_port.read(132)
    else:
        packet = serial_port.read(133)

    if len(packet) == 0:
        raise SenderDoesNotAcceptTransferException

    packet_number = 1
    response = None
    while response != EOT:

        if packet[1] != SOH:
            raise WrongHeaderException
        elif packet_number % 255 != packet[2]:
            raise WrongPacketNumberException

        block = None
        message_sum = None
        if check_sum_type == CheckSumEnum.algebraic:
            block = packet[2:-1]
            message_sum = packet[-1]
            calculated_sum = check_sum.algebraic_check_sum(block)
        else:
            block = packet[2:-2]
            message_sum = packet[-2:]
            calculated_sum = check_sum.crc_check_sum(block)

        if message_sum != calculated_sum:
            raise WrongCheckSumException
