# Multiplayer logic.
# Keeps track of all running games, and is the interface between the network and the game engine.

from uuid import uuid4

from .engine.constants import MAX_PLAYERS, GameState
from .engine.main import ScotlandYard

GAMES: dict[str, ScotlandYard] = {}
PLAYER_TO_GAME: dict[str, str] = {}


def get_game_by_id(game_id: str) -> ScotlandYard:
    if game_id not in GAMES:
        raise ValueError(f"invalid game ID {game_id}")
    game = GAMES[game_id]
    return game


def get_game_id_with_player(player_id: str) -> str:
    id = PLAYER_TO_GAME[player_id] if player_id in PLAYER_TO_GAME else None
    if id is not None and id not in GAMES:
        del PLAYER_TO_GAME[player_id]
        return None
    return id


def get_game_state(game_id: str) -> GameState:
    return get_game_by_id(game_id).state


def get_player_connected_game(player_id: str) -> str:
    game_id = get_game_id_with_player(player_id)
    return (
        game_id
        if game_id is not None and GAMES[game_id].state != GameState.STOPPED
        else None
    )


def get_player_info(game_id: str, player_id: str) -> dict:
    return get_game_by_id(game_id).get_player_info(player_id)


def get_player_ids(game_id: str) -> list[str]:
    return get_game_by_id(game_id).get_player_ids()


def get_game_host(game_id: str) -> str:
    return get_game_by_id(game_id).get_host_id()


def get_game_info(game_id: str) -> dict:
    return get_game_by_id(game_id).get_game_info()


def get_mr_x(game_id: str) -> str:
    return get_game_by_id(game_id).get_mr_x()


def create_room() -> str:
    game_id = str(uuid4())
    game = ScotlandYard(game_id)
    GAMES[game_id] = game
    print(f"created room {game_id}")
    return game_id


def join_room(game_id: str, player_id: str, player_name: str):
    print(f"{player_name} is joining {game_id}... ")
    game = get_game_by_id(game_id)
    game.add_player(player_id, player_name)
    PLAYER_TO_GAME[player_id] = game_id


def set_mr_x(game_id: str, player_id: str):
    get_game_by_id(game_id).set_mr_x(player_id)


def set_color(game_id: str, player_id: str, color: str):
    get_game_by_id(game_id).set_color(player_id, color)


def start_game(game_id: str):
    get_game_by_id(game_id).start()


def start_roll_call(game_id: str):
    get_game_by_id(game_id).state = GameState.CONNECTING


def answer_roll_call(game_id: str, player_id: str):
    if get_game_id_with_player(player_id) != game_id:
        raise ValueError("This player id does not exist in this game")
    game = get_game_by_id(game_id)
    game.rollCall.add(player_id)
    print(f"{player_id} answered roll call ({len(game.rollCall)} of 6)")
    if len(game.rollCall) == MAX_PLAYERS:
        start_game(game_id)


def move(game_id: str, player_id: str, ticket: str, data: dict):
    game = get_game_by_id(game_id)
    if game.state != GameState.RUNNING:
        raise ValueError("Game is not running")
    return game.request_move(player_id, ticket, data)


def leave_room(game_id: str, player_id: str):
    game = get_game_by_id(game_id)
    if game.state != GameState.CONNECTING:
        del PLAYER_TO_GAME[player_id]
        game.remove_player(player_id)
        print(f"removed {player_id} from {game_id}")


def delete_game(game_id: str):
    for p in get_player_ids(game_id):
        del PLAYER_TO_GAME[p]
    del GAMES[game_id]
