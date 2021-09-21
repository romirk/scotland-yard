from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader


def index(request):
    template = loader.get_template('scotlandyardgame/index.html')
    context = {
        'action': '/',
        'game_id': 'game_id',
        'isjoining': False
    }
    if request.method == "POST":
        print(request.POST)
    return render(request, 'scotlandyardgame/index.html', context=context)


def lobby(request):
    context = {
        'action': '/',
        'game_id': 'game_id',
        'isjoining': False,
        'player_id': 'player_id',
        'name': 'name',
        'color': 'color',
        'isMrX': "false"
    }
    return render(request, 'scotlandyardgame/lobby.html', context=context)
