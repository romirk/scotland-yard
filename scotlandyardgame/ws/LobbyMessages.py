from scotlandyardgame.ws.messages import Messages

from ..multiplayer import getGameIDWithPlayer, getPlayerIDs, getPlayerInfo


class LobbyMessages(Messages):
    """
    LobbyMessages is a class that handles all the messages that are sent to the client while they are connected to a lobby.
    """

    @staticmethod
    def acknowledge(game_id: str, track_disconnected: list[str]) -> str:
        """acknowledge ws connection"""
        players = [
            getPlayerInfo(getGameIDWithPlayer(p), p)
            for p in getPlayerIDs(game_id)
            if p not in track_disconnected
        ]
        return f"ACKNOWLEDGE {len(players)}\n" + "\n".join(
            f"{p_info['player_id']} {p_info['name']} {p_info['color']} {p_info['is_host']}"
            for p_info in players
        )

    @staticmethod
    def player_joined(player_id: str) -> str:
        """notify lobby of new player"""
        player_info = getPlayerInfo(getGameIDWithPlayer(player_id), player_id)
        return f"PLAYER_JOINED {player_id} {player_info['name']} {player_info['color']} {player_info['is_host']}"

    @staticmethod
    def set_color(player_id: str, new_color: str) -> str:
        """set player's color for the lobby"""
        return f"SET_COLOR {player_id} {new_color}"

    @staticmethod
    def start_game():
        """issue game start command"""
        return "STARTGAME"
