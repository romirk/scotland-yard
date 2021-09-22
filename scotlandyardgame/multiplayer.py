from .engine.main import ScotlandYard
from uuid import uuid4

games: dict[str, ScotlandYard] = {}
player_games: dict[str, str] = {}


def createRoom() -> str:
    game_id = str(uuid4())
    game = ScotlandYard(game_id)
    games[game_id] = game
    print(f"created room {game_id}")
    return game_id


def joinRoom(game_id: str, player_id: str, player_name: str):
    print(f"{player_name} is joining {game_id}... ")
    if game_id not in games:
        raise ValueError(f"invalid game ID {game_id}")
    games[game_id].addPlayer(player_id, player_name)
    player_games[player_id] = game_id


def getGameWithPlayer(player_id: str) -> str:
    return player_games[player_id] if player_id in player_games else None
