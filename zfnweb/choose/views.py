from django.shortcuts import render
from django.http import HttpResponse

def Index():
    return HttpResponse('choose_index here')