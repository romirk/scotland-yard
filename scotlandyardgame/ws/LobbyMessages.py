from ..multiplayer import getPlayerIDs, getPlayerInfo


class LobbyMessages:
    @staticmethod
    def acknowledge(game_id: str) -> str:
        """acknowledge ws connection"""
        players = [getPlayerInfo(p) for p in getPlayerIDs(
            game_id) if p not in LobbyMessages.trackdisconnected]
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
    def setHost(player_id: str) -> dict:
        """set player to lobby host"""
        return f"SET_HOST {player_id}"

    @staticmethod
    def setMrX(player_id: str) -> dict:
        """set player to Mr. X for the lobby"""
        return f"SET_MRX {player_id}"

    @staticmethod
    def startGame():
        """issue game start command"""
        return "STARTGAME"

    @staticmethod
    def LOS(player_id: str):
        """report LOs"""
        return f"LOS {player_id}"

    @staticmethod
    def remove(player_id: str):
        """remove player from lobby"""
        return f"DISCONNECT {player_id}"

    @staticmethod
    def abort():
        """abort game"""
        return f"ABORT"
