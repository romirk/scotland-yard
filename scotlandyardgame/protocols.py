from __future__ import annotations

from .multiplayer import getGameByID, getPlayerIDs, getPlayerInfo


class LobbyProtocol:
    ACCEPTED_KEYWORDS = ["JOIN", "REQCOLOR", "REQMRX", "READY", "DISCONNECT"]

    def __init__(self, type: str, player_id: str) -> None:
        # purely for returning from parser
        self.type = type
        self.player_id = player_id
        self.color = None
        self.target = None

    @staticmethod
    def parse(msg: str) -> LobbyProtocol:
        """parse incoming ws client message"""
        tokens = msg.split()
        keyword = tokens[0]

        if len(tokens) < 2 or keyword not in LobbyProtocol.ACCEPTED_KEYWORDS:
            raise ValueError(f"invalid message: {msg}")

        ret = LobbyProtocol(keyword, tokens[1])

        if keyword == "REQCOLOR":
            ret.color = tokens[2]
        elif keyword == "REQMRX":
            ret.target = tokens[2]

        return ret

    @staticmethod
    def acknowledge(game_id: str) -> str:
        """acknowledge ws connection"""
        players = [getPlayerInfo(p) for p in getPlayerIDs(game_id) if p not in LobbyProtocol.trackdisconnected]
        return f"ACKNOWLEDGE {len(players)}\n" + "\n".join(
            f"{p_info['player_id']} {p_info['name']} {p_info['color']} {p_info['is_host']}" for p_info in players
        )

    @staticmethod
    def newPlayer(player_id: str) -> dict:
        """Group method: notify lobby of new player"""
        playerInfo = getPlayerInfo(player_id)
        return {
            "type": "ws.send",
            "text": f"NEW_PLAYER {player_id} {playerInfo['name']} {playerInfo['color']} {playerInfo['is_host']}"
        }

    @staticmethod
    def setColor(player_id: str, newColor: str) -> dict:
        """set player's color for the lobby"""
        return {
            "type": "ws.send",
            "text": f"SET_COLOR {player_id} {newColor}"
        }

    @staticmethod
    def setHost(player_id: str) -> dict:
        """set player to lobby host"""
        return {
            "type": "ws.send",
            "text": f"SET_HOST {player_id}"
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
    def LOS(player_id: str):
        """report LOs"""
        return {
            "type": "ws.send",
            "text": f"LOS {player_id}"
        }

    @staticmethod
    def remove(player_id: str):
        """remove player from lobby"""
        return {
            "type": "ws.send",
            "text": f"DISCONNECT {player_id}"
        }

    @staticmethod
    def abort():
        """abort game"""
        return {
            "type": "ws.send",
            "text": f"ABORT"
        }

class GameProtocol:
    # TODO GameProtocol
    ACCEPTED_KEYWORDS = ["JOIN", "REQMOVE"]

    def __init__(self, type: str, player_id: str) -> None:
        # purely for returning from parser
        self.type = type
        self.player_id = player_id
        self.destination = None

    @staticmethod
    def parse(msg: str) -> GameProtocol:
        """
        parse incoming ws client message

        For Double Moves:
        ret.double = ((Ticket 1, Destination 1),(Ticket 2, Destination  2))
        """
        tokens = msg.split()
        keyword = tokens[0]

        # if len(tokens) < 2 or keyword not in GameProtocol.ACCEPTED_KEYWORDS:
        #     raise ValueError("invalid message")

        ret = GameProtocol(keyword, tokens[1])

        if keyword == "JOIN":
            pass
        elif keyword == "REQMOVE":
            ret.ticket = tokens[2]          
            if ret.ticket == "double":
                ret.double = ((tokens[3],int(tokens[4])),(tokens[5],int(tokens[6]))) 
            else:
                ret.destination = int(tokens[3])

        return ret

    @staticmethod
    def playerJoined(player_id: str) -> dict:
        return {
            "type": "ws.send",
            "text": f"PLAYER_JOINED {player_id}"
        }

    @staticmethod
    def acknowledge(game_id: str) -> str:
        roll = getGameByID(game_id).rollCall
        return "ACKNOWLEDGE " + " ".join(roll)

    @staticmethod
    def gameStarting() -> dict:
        return {
            "type": "ws.send",
            "text": f"GAME_STARTING"
        }
