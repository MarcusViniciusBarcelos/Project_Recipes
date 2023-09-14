from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return render(request, 'recipes/pages/home.html', {
        'name': 'Marcus'
    })


def recipe(request, id):
    return render(request, 'recipes/pages/recipe-view.html', {
        'name': 'Marcus'
    })
