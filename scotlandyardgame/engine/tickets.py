from .constants import (
    TAXI_TICKET,
    BUS_TICKET,
    TICKET_TYPES,
    UNDERGROUND_TICKET,
    BLACK_TICKET,
    DOUBLE_TICKET,
)


class Tickets:
    def __init__(self, is_mr_x: bool) -> None:
        self.__is_mr_x = is_mr_x

        if is_mr_x:
            self.__taxi = 4
            self.__bus = 3
            self.__underground = 3
            self.__black = 5
            self.__double = 2
        else:
            self.__taxi = 10
            self.__bus = 8
            self.__underground = 4

    def discard(self, ticket_type: str) -> None:
        if ticket_type == TAXI_TICKET:
            self.__taxi -= 1
        elif ticket_type == BUS_TICKET:
            self.__bus -= 1
        elif ticket_type == UNDERGROUND_TICKET:
            self.__underground -= 1
        elif ticket_type == BLACK_TICKET:
            self.__black -= 1
        elif ticket_type == DOUBLE_TICKET:
            self.__double -= 1
        else:
            raise ValueError("Invalid ticket type: {}".format(ticket_type))

    def gain(self, ticket_type: str) -> None:
        if not self.__is_mr_x:
            return
        if ticket_type == TAXI_TICKET:
            self.__taxi += 1
        elif ticket_type == BUS_TICKET:
            self.__bus += 1
        elif ticket_type == UNDERGROUND_TICKET:
            self.__underground += 1
        elif ticket_type == BLACK_TICKET and self.__is_mr_x:
            self.__black += 1
        elif ticket_type == DOUBLE_TICKET and self.__is_mr_x:
            self.__double += 1
        else:
            raise ValueError("Invalid ticket type: {}".format(ticket_type))

    def all(self) -> dict[str, int]:
        return {
            TAXI_TICKET: self.__taxi,
            BUS_TICKET: self.__bus,
            UNDERGROUND_TICKET: self.__underground,
            BLACK_TICKET: self.__black if self.__is_mr_x else 0,
            DOUBLE_TICKET: self.__double if self.__is_mr_x else 0,
        }

    def get(self, ticket: str):
        if ticket not in TICKET_TYPES:
            raise ValueError("Invalid ticket type: {}".format(ticket))
        return self.all()[ticket]

    def set(self, tickets: dict[str, int]):
        self.__taxi = tickets[TAXI_TICKET]
        self.__bus = tickets[BUS_TICKET]
        self.__underground = tickets[UNDERGROUND_TICKET]
        if self.__is_mr_x:
            self.__black = tickets[BLACK_TICKET]
            self.__double = tickets[DOUBLE_TICKET]

    def __str__(self) -> str:
        return str(self.all())
