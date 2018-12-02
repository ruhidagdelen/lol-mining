from django.shortcuts import render
from django.http import HttpResponse
from .forms import PlayerForm

def index(request):
    if request.method == "POST":
        form = PlayerForm(request.POST)
        if form.is_valid():
            player = form.save(commit=False)
            player.save()
            result = calculate(player)
            return render(request, 'results/results.html',{'result':result})
    else:
        form = PlayerForm()
    return render(request, 'results/index.html', {'form':form})

def about(request):
    return render(request, 'results/about.html', {})

def how_to(request):
    return render(request, 'results/how_to.html', {})

def calculate(player):
    return player.username

