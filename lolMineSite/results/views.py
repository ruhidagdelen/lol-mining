from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	return HttpResponse("this is index page")

def about(request):
	return HttpResponse("this is about page")

def how_to(request):
	return HttpResponse("this is expalin of how to?")

def results(request):
	return HttpResponse("this is where we will show the results")

