from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	return render(request, 'results/index.html', {})

def about(request):
	return render(request, 'results/about.html', {})

def how_to(request):
	return render(request, 'results/how_to.html', {})

def results(request):
	return render(request, 'results/results.html', {})

