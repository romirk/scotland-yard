class Player:

    def __init__(self, player_id: str, player_name: str, player_location: int, player_color: str, is_mr_x: bool) -> None:
        # private
        self.__player_id: str = player_id
        self.__player_location: int = player_location
        self.__is_mr_x: bool = is_mr_x
        self.__tickets: dict[str, int] = {
            "taxi": 4,
            "bus": 3,
            "underground": 3,
            "black": 5,
            "times_two": 2
        } if is_mr_x else {
            "taxi": 10,
            "bus": 8,
            "underground": 4
        }

        # public
        self.name: str = player_name
        self.color: str = player_color

    # getters

    @property
    def ID(self) -> str:
        return self.__player_id

    @property
    def location(self) -> int:
        return self.__player_location

    @property
    def is_mr_x(self) -> bool:
        return self.__is_mr_x

    # setters

    @ID.setter
    def ID(self, newID: str):
        raise AttributeError("ID assignment not allowed.")

    @location.setter
    def location(self, newLocation: int):
        self.__player_location = newLocation if 1 <= newLocation <= 200 else self.__player_location

    @is_mr_x.setter
    def is_mr_x(self, value: bool, color: str = 'X'):
        if not value and color == 'X':
            raise ValueError("cannot assign color X to non-Mr. X Player.")
        self.__is_mr_x = value
        self.color = 'X' if value else color

    # methods

    def getTickets(self, type: str) -> int:
        """returns number of tickets of type ```type``` available to this player."""
        return self.__tickets[type]

    def discard(self, type):
        """player uses a ticket."""
        self.__tickets[type] -= 1 if self.__tickets[type] else 0

    def gain(self, type):
        if not self.is_mr_x:
            raise TypeError("non-Mr. X Player cannot gain a ticket.")
        if type not in ["taxi", "bus", "underground"]:
            raise ValueError(f"cannot gain ticket of type '{type}.'")
        self.__tickets[type] -= 1
