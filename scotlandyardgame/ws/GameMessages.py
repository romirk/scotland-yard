from ast import Str
import json

from ..engine.constants import DOUBLE_TICKET
from ..multiplayer import getGameByID, getPlayerInfo, getGameIDWithPlayer


class GameMessages:
    """
    GameMessages is a class that handles all the messages that are sent to the client during a game.
    """

    @staticmethod
    def playerJoined(player_id: str) -> str:
        player_info = getPlayerInfo(getGameIDWithPlayer(player_id), player_id)
        return f"PLAYER_JOINED {player_id}" + (
            f' {player_info["location"]}' if player_info["color"] != "X" else ""
        )

    @staticmethod
    def acknowledge(game_id: str) -> str:
        roll = getGameByID(game_id).rollCall
        return "ACKNOWLEDGE " + " ".join(roll)

    @staticmethod
    def gameStarting() -> str:
        return f"GAME_STARTING"

    @staticmethod
    def playerMoved(move_info: dict) -> dict:
        return_msg = f'PLAYER_MOVED {move_info["player_id"]} {move_info["cycle_number"]} {move_info["ticket"]} '
        if move_info["is_mr_x"]:
            if move_info["ticket"] == DOUBLE_TICKET:
                return_msg += (
                    f'{move_info["double_tickets"][0]} {move_info["double_tickets"][1]} '
                )
            if move_info["is_surface_move"]:
                return_msg += str(move_info["destination"])

        else:
            return_msg += str(move_info["destination"])

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
