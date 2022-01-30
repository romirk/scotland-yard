import json

from ..engine.constants import DOUBLE_TICKET
from ..multiplayer import getGameByID, getPlayerInfo, getGameIDWithPlayer


class GameMessages:
    """
    GameMessages is a class that handles all the messages that are sent to the client during a game.
    """

    @staticmethod
    def playerJoined(player_id: str) -> dict:
        player_info = getPlayerInfo(getGameIDWithPlayer(player_id), player_id)
        return f"PLAYER_JOINED {player_id}" + (
            f' {player_info["location"]}' if player_info["color"] != "X" else ""
        )

    @staticmethod
    def acknowledge(game_id: str) -> str:
        roll = getGameByID(game_id).rollCall
        return "ACKNOWLEDGE " + " ".join(roll)

    @staticmethod
    def gameStarting() -> dict:
        return f"GAME_STARTING"

    @staticmethod
    def playerMoved(moveMade: dict) -> dict:
        return_msg = f'PLAYER_MOVED {moveMade["player_id"]} {moveMade["cycle_number"]} {moveMade["ticket"]} '
        if moveMade["is_mr_x"]:
            if moveMade["ticket"] == DOUBLE_TICKET:
                return_msg += (
                    f'{moveMade["double_tickets"][0]} {moveMade["double_tickets"][1]} '
                )
            if moveMade["is_surface_move"]:
                return_msg += str(moveMade["destination"])

        else:
            return_msg += str(moveMade["destination"])

        return return_msg

    @staticmethod
    def updateMrX(destination: int) -> str:
        return f"UPDATE_X {destination}"

    @staticmethod
    def gameInfo(info: dict) -> str:
        return "GAME_INFO " + json.dumps(info)

    @staticmethod
    def playerInfo(info: dict) -> str:
        return "PLAYER_INFO " + json.dumps(info)
