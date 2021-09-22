from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.template import loader
from . import multiplayer


def index(request: HttpRequest):
    template = loader.get_template('scotlandyardgame/index.html')
    context = {
        'action': '/',
        'game_id': '',
        'isJoining': "false"
    }
    if request.method == "POST":
        player_id = request.session["player_id"]
        player_name = request.POST["player_name"]
        game_id = multiplayer.createRoom()
        multiplayer.games[game_id].addPlayer(player_id, player_name)
    return render(request, 'scotlandyardgame/index.html', context=context)


def lobby(request: HttpRequest):
    player_id = request.session["player_id"]
    game_id = multiplayer.getGameWithPlayer(player_id)
    player = multiplayer.games[game_id].getPlayerByID(player_id)
    context = {
        'game_id': game_id,
        'player_id': player_id,
        'name': player.name,
        'color': player.color,
        'isMrX': player.is_mr_x
    }
    return render(request, 'scotlandyardgame/lobby.html', context=context)


def join(request, game_id):
    context = {
        'action': '/lobby',
        'game_id': game_id,
        'isJoining': "true"
    }
    return render(request, 'scotlandyardgame/index.html', context=context)


def new(request):
    game_id = multiplayer.createRoom()
    return redirect('/lobby')
