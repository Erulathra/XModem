import check_sum as cs
import serial as ser

import xmodem


def main():
    user_input = ""
    while user_input != "q":
        user_input = input('''Podaj, czy chcesz:
        (1) Wysłać pakiet
        (2) Odebrać pakiet
        [q - wyjście]\n> ''')
        match user_input:
            case '1': send_packet()
            case '2': receive_packet()
            case _: continue


def send_packet():
    message = ""
    # read user input
    match input("Wiadomość:\n\t(1) Predefiniowana\n\t(2) Wpisana ręcznie\n\t(3) Z pliku\n> "):
        case '1':
            message = Examples.invocation
        case '2':
            message = input("Podaj wiadomość: ")
        case '3':
            message = message_from_file(input("Podaj ścieżkę: "))

    # initialize port and send message
    port_name = "/dev/pts/3"
    baudrate = 9600
    timeout = 3

    serial_port = xmodem.initialize_serial(port_name, baudrate)
    xmodem.send(serial_port, bytes(message, 'ascii'))

    serial_port.close()


def receive_packet():
    port_name = "/dev/pts/4"
    baudrate = 9600

    serial_port = xmodem.initialize_serial(port_name, baudrate)
    data = xmodem.receive(serial_port, xmodem.CheckSumEnum.crc)
    print("Cała wiadomość: ")
    print(data.decode("utf-8"))
    serial_port.close()


def message_from_file(path):
	with open(path, "r") as message_file:
		result = ""
		for line in message_file:
			result += line
	return result


class Examples:
    invocation = "Litwo! Ojczyzno moja! Ty jestes jak zdrowie," \
           "Ile cie trzeba cenic, ten tylko sie dowie," \
           "Kto cie stracil. Dzis pieknosc twa w calej ozdobie " \
           "Widze i opisuje, bo tesknie po tobie " \
           "Panno swieta, co Jasnej bronisz Czestochowy " \
           "I w Ostrej swiecisz Bramie! Ty, co grod zamkowy " \
           "Nowogrodzki ochraniasz z jego wiernym ludem! " \
           "Jak mnie dziecko do zdrowia powrocilas cudem, " \
           "(Gdy od placzacej matki pod Twoja opieke " \
           "Ofiarowany, martwa podnioslem powieke " \
           "I zaraz moglem pieszo do Twych swiatyn progu " \
           "Isc za wrocone zycie podziekowac Bogu), " \
           "Tak nas powrocisz cudem na Ojczyzny lono. " \
           "Tymczasem przenos moja dusze uteskniona " \
           "Do tych pagorkow lesnych, do tych lak zielonych, " \
           "Szeroko nad blekitnym Niemnem rozciagnionych; " \
           "Do tych pol malowanych zbozem rozmaitem, " \
           "Wyzlacanych pszenica, posrebrzanych zytem; " \
           "Gdzie bursztynowy swierzop, gryka jak snieg biala, " \
           "Gdzie panienskim rumiencem dziecielina pala, " \
           "A wszystko przepasane jakby wstega, miedza " \
           "Zielona, na niej z rzadka ciche grusze siedza."

if __name__ == "__main__":
    main()
