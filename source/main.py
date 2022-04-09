import check_sum as cs


def main():
    test = "ziemniaki sa fajne i mozna je wrzucic do stringa, a ja musze zrobic 128 bajtowego stringa wiec mi sie " \
           "przydadza, jeszcze tylko a "

    print(cs.algebraic_check_sum(bytes(test, "ascii")))
    print(cs.crc_check_sum(bytes(test, "ascii")))


if __name__ == "__main__":
    main()