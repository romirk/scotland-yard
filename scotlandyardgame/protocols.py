from __future__ import annotations
from .multiplayer import getPlayerInfo, getPlayerIDs


class LobbyProtocol:
    ACCEPTED_KEYWORDS = ["JOIN", "REQCOLOR", "REQMRX"]

    def __init__(self, type: str, player_id: str) -> None:
        # purely for returning from parser
        self.type = type
        self.player_id = player_id
        self.color = None

    def parse(msg: str) -> LobbyProtocol:
        tokens = msg.split()
        keyword = tokens[0]

        if len(tokens) < 2 or keyword not in LobbyProtocol.ACCEPTED_KEYWORDS:
            raise ValueError("invalid message")

        ret = LobbyProtocol(keyword, tokens[1])

        if keyword == "REQCOLOR":
            ret.color = tokens[2]

        return ret

    def acknowledge(game_id: str):
        connected_players = [getPlayerInfo(p) for p in getPlayerIDs(game_id)]
        return f"ACKNOWLEDGE {len(connected_players)}" + "\n".join(
            f"{p_info['player_id']} {p_info['name']} {p_info['color']} {p_info['is_mr_x']}" for p_info in connected_players
        )

    def newPlayer(game_id: str, player_id: str):
        playerInfo = getPlayerInfo(player_id)
        f"NEW_PLAYER {player_id} {playerInfo['name']} {playerInfo['color']} {playerInfo['is_mr_x']}"
