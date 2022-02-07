from uuid import uuid4

from .engine.constants import MAX_PLAYERS, GameState
from .engine.main import ScotlandYard

GAMES: dict[str, ScotlandYard] = {}
PLAYER_TO_GAME: dict[str, str] = {}


def getGameByID(game_id: str) -> ScotlandYard:
    if game_id not in GAMES:
        raise ValueError(f"invalid game ID {game_id}")
    game = GAMES[game_id]
    return game


def getGameIDWithPlayer(player_id: str) -> str:
    id = PLAYER_TO_GAME[player_id] if player_id in PLAYER_TO_GAME else None
    if id is not None and id not in GAMES:
        del PLAYER_TO_GAME[player_id]
        return None
    return id


def getGameState(game_id: str) -> GameState:
    return getGameByID(game_id).state


def getPlayerConnectedGame(player_id: str) -> str:
    game_id = getGameIDWithPlayer(player_id)
    return (
        game_id
        if game_id is not None and GAMES[game_id].state != GameState.STOPPED
        else None
    )


def getPlayerInfo(game_id: str, player_id: str) -> dict:
    return getGameByID(game_id).getPlayerInfo(player_id)


def getPlayerIDs(game_id: str) -> list[str]:
    return getGameByID(game_id).getPlayerIDs()


def getGameHost(game_id: str) -> str:
    return getGameByID(game_id).getHostID()


def getGameInfo(game_id: str) -> dict:
    return getGameByID(game_id).getGameInfo()


def getMrX(game_id: str) -> str:
    return getGameByID(game_id).getMrX()


def createRoom() -> str:
    game_id = str(uuid4())
    game = ScotlandYard(game_id)
    GAMES[game_id] = game
    print(f"created room {game_id}")
    return game_id


def joinRoom(game_id: str, player_id: str, player_name: str):
    print(f"{player_name} is joining {game_id}... ")
    game = getGameByID(game_id)
    game.addPlayer(player_id, player_name)
    PLAYER_TO_GAME[player_id] = game_id


def setMrX(game_id: str, player_id: str):
    getGameByID(game_id).setMrX(player_id)


def setColor(game_id: str, player_id: str, color: str):
    getGameByID(game_id).setColor(player_id, color)


def startGame(game_id: str):
    getGameByID(game_id).start()


def startRollCall(game_id: str):
    getGameByID(game_id).state = GameState.CONNECTING


def answerRollCall(game_id: str, player_id: str):
    if getGameIDWithPlayer(player_id) != game_id:
        raise ValueError("This player id does not exist in this game")
    game = getGameByID(game_id)
    game.rollCall.add(player_id)
    print(f"{player_id} answered roll call ({len(game.rollCall)} of 6)")
    if len(game.rollCall) == MAX_PLAYERS:
        startGame(game_id)


def move(game_id: str, player_id: str, ticket: str, data: dict):
    game = getGameByID(game_id)
    if game.state != GameState.RUNNING:
        raise ValueError("Game is not running")
    return game.requestMove(player_id, ticket, data)


def leaveRoom(game_id: str, player_id: str):
    game = getGameByID(game_id)
    if game.state != GameState.CONNECTING:
        del PLAYER_TO_GAME[player_id]
        game.removePlayer(player_id)
        print(f"removed {player_id} from {game_id}")


def deleteGame(game_id: str):
    for p in getPlayerIDs(game_id):
        del PLAYER_TO_GAME[p]
    del GAMES[game_id]
