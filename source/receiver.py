import check_sum as cs
import serial as ser

import xmodem


def main():
    test = "Litwo! Ojczyzno moja! Ty jestes jak zdrowie," \
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

    port_name = "/dev/pts/4"
    baudrate = 9600

    serial_port = xmodem.initialize_serial(port_name, baudrate)
    data = xmodem.receive(serial_port, xmodem.CheckSumEnum.algebraic)
    print("Cała wiadomość: ")
    print(data.decode("ascii"))
    serial_port.close()


if __name__ == "__main__":
    main()