import json

from ..engine.constants import DOUBLE_TICKET
from ..multiplayer import get_game_by_id, get_player_info, get_game_id_with_player


class GameMessages:
    """
    GameMessages is a class that handles all the messages that are sent to the client during a game.
    """

    @staticmethod
    def player_joined(player_id: str) -> str:
        player_info = get_player_info(get_game_id_with_player(player_id), player_id)[player_id]
        return f"PLAYER_JOINED {player_id}" + (
            f' {player_info["location"]}' if player_info["color"] != "X" else ""
        )

    @staticmethod
    def acknowledge(game_id: str, t: list) -> str:
        roll = get_game_by_id(game_id).rollCall
        return "ACKNOWLEDGE " + " ".join(roll)

    @staticmethod
    def game_starting() -> str:
        return f"GAME_STARTING"

    @staticmethod
    def player_moved(move_info: dict) -> dict:
        return_msg = f'PLAYER_MOVED {move_info["player_id"]} {move_info["cycle_number"]} {move_info["ticket"]} '
        if move_info["is_mr_x"]:
            if move_info["ticket"] == DOUBLE_TICKET:
                return_msg += f'{move_info["double_tickets"][0]} {move_info["double_tickets"][1]} '
            if move_info["is_surface_move"]:
                return_msg += str(move_info["destination"])

        else:
            return_msg += str(move_info["destination"])

        return return_msg

    @staticmethod
    def update_mr_x(destination: int) -> str:
        return f"UPDATE_X {destination}"

    @staticmethod
    def game_info(info: dict) -> str:
        return "GAME_INFO " + json.dumps(info)

    @staticmethod
    def player_info(info: dict) -> str:
        return "PLAYER_INFO " + json.dumps(info)

    @staticmethod
    def help(fmap: dict) -> str:
        return "HELP\n" + "\n".join(f"{k}\t{v.__doc__}" for k, v in fmap.items())
