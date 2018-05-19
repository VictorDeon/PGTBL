from django.shortcuts import render
from django.http import HttpResponse

def peer(request):
    return HttpResponse("Tela da Avaliação em Pares")