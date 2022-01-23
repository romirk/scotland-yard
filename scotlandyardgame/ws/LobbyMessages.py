from scotlandyardgame.ws.messages import Messages
from ..multiplayer import getPlayerIDs, getPlayerInfo
from .WebSocketConsumer import TRACK_DISCONNECTED


class LobbyMessages(Messages):
    @staticmethod
    def acknowledge(game_id: str) -> str:
        """acknowledge ws connection"""
        players = [getPlayerInfo(p) for p in getPlayerIDs(
            game_id) if p not in TRACK_DISCONNECTED]
        return f"ACKNOWLEDGE {len(players)}\n" + "\n".join(
            f"{p_info['player_id']} {p_info['name']} {p_info['color']} {p_info['is_host']}" for p_info in players
        )

    @staticmethod
    def newPlayer(player_id: str) -> str:
        """notify lobby of new player"""
        playerInfo = getPlayerInfo(player_id)
        return f"NEW_PLAYER {player_id} {playerInfo['name']} {playerInfo['color']} {playerInfo['is_host']}"

    @staticmethod
    def setColor(player_id: str, newColor: str) -> dict:
        """set player's color for the lobby"""
        return f"SET_COLOR {player_id} {newColor}"

    @staticmethod
    def startGame():
        """issue game start command"""
        return "STARTGAME"
