from typing import Final

from .tickets import Tickets


class Player:
    def __init__(
        self, player_id: str, player_name: str, player_location: int, player_color: str
    ) -> None:
        # private
        self.__ID: Final = player_id
        self.__player_location: int = player_location
        self.__tickets: Tickets = Tickets(player_color == "X")

        # public
        self.name: str = player_name
        self.color: str = player_color

    # getters

    @property
    def id(self) -> str:
        return self.__ID

    @property
    def location(self) -> int:
        return self.__player_location

    @property
    def is_mr_x(self) -> bool:
        return self.color == "X"

    @property
    def tickets(self) -> Tickets:
        """returns all tickets available to this player."""
        return self.__tickets

    # setters

    @id.setter
    def id(self, *args):
        raise AttributeError("ID assignment not allowed.")

    @location.setter
    def location(self, new_location: int):
        self.__player_location = (
            new_location if 1 <= new_location <= 200 else self.__player_location
        )
