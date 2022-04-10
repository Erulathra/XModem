from enum import Enum

import serial as ser
from check_sum import algebraic_check_sum, crc_check_sum

SOH = b'\x01'
EOT = b'\x04'
ACK = b'\x06'
NAK = b'\x15'
CAN = b'\x18'
SUB = b'\x1A'
CRC = b'\x43'


class CheckSumEnum(Enum):
    algebraic = 0
    CRC = 1


def prepare_packets(data: bytes, check_sum: CheckSumEnum) -> [bytes]:
    # split data intro 128 bytes long blocks
    blocks = [data[i:i + 128] for i in range(0, len(data), 128)]

    packets = []
    for packet_number in range(len(blocks)):
        packet = bytearray()

        if check_sum == CheckSumEnum.algebraic:
            packet += bytearray(SOH)
        elif check_sum == CheckSumEnum.CRC:
            packet += bytearray(CRC)

        # append packet number and it's compliment
        packet.append(packet_number % 255)
        packet.append(255 - (packet_number % 255))

        # append data block
        packet += bytearray(blocks[packet_number])

        # calculate check sum
        calculated_check_sum = None
        if check_sum == CheckSumEnum.algebraic:
            calculated_check_sum = algebraic_check_sum(blocks[packet_number])
        elif check_sum == CheckSumEnum.CRC:
            calculated_check_sum = crc_check_sum(blocks[packet_number])

        # and append it to packet
        packet += bytearray(calculated_check_sum)

        # append packet to packet list
        packets.append(bytes(packet))

    return packets

