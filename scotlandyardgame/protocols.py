from __future__ import annotations

from .multiplayer import getPlayerIDs, getPlayerInfo


class LobbyProtocol:
    ACCEPTED_KEYWORDS = ["JOIN", "REQCOLOR", "REQMRX", "READY"]

    def __init__(self, type: str, player_id: str) -> None:
        # purely for returning from parser
        self.type = type
        self.player_id = player_id
        self.color = None

    @staticmethod
    def parse(msg: str) -> LobbyProtocol:
        """parse incoming ws client message"""
        tokens = msg.split()
        keyword = tokens[0]

        if len(tokens) < 2 or keyword not in LobbyProtocol.ACCEPTED_KEYWORDS:
            raise ValueError("invalid message")

        ret = LobbyProtocol(keyword, tokens[1])

        if keyword == "REQCOLOR":
            ret.color = tokens[2]

        return ret

    @staticmethod
    def acknowledge(game_id: str) -> str:
        """acknowledge ws connection"""
        players = [getPlayerInfo(p) for p in getPlayerIDs(game_id)]
        return f"ACKNOWLEDGE {len(players)}\n" + "\n".join(
            f"{p_info['player_id']} {p_info['name']} {p_info['color']}" for p_info in players
        )

    @staticmethod
    def newPlayer(player_id: str) -> dict:
        """Group method: notify lobby of new player"""
        playerInfo = getPlayerInfo(player_id)
        return {
            "type": "ws.send",
            "text": f"NEW_PLAYER {player_id} {playerInfo['name']} {playerInfo['color']}"
        }

    @staticmethod
    def setColor(player_id: str, newColor: str) -> dict:
        """set player's color for the lobby"""
        return {
            "type": "ws.send",
            "text": f"SET_COLOR {player_id} {newColor}"
        }

    @staticmethod
    def setMrX(player_id: str) -> dict:
        """set player to Mr. X for the lobby"""
        return {
            "type": "ws.send",
            "text": f"SET_MRX {player_id}"
        }

    @staticmethod
    def startGame():
        """issue game start command"""
        return {
            "type": "ws.send",
            "text": "STARTGAME"
        }

    @staticmethod
    def remove(player_id: str):
        """remove player from lobby"""
        return {
            "type": "ws.send",
            "text": f"DISCONNECT {player_id}"
        }


class GameProtocol:
    # TODO GameProtocol
    ACCEPTED_KEYWORDS = ["JOIN", "READY"]

    def __init__(self, type: str, player_id: str) -> None:
        # purely for returning from parser
        self.type = type
        self.player_id = player_id
        self.color = None

    @staticmethod
    def parse(msg: str) -> LobbyProtocol:
        """parse incoming ws client message"""
        tokens = msg.split()
        keyword = tokens[0]

        if len(tokens) < 2 or keyword not in LobbyProtocol.ACCEPTED_KEYWORDS:
            raise ValueError("invalid message")

        ret = LobbyProtocol(keyword, tokens[1])

        return ret
