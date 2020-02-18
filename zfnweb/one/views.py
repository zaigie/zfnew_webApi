from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import os
import json
from bs4 import BeautifulSoup
import requests
import re
import datetime

def get_one(request):
    url = "http://wufazhuce.com/"
    r = requests.get(url)
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, 'html.parser')
    oneall = soup.find('div',class_ = re.compile('fp-one-cita'))
    one = oneall.a.string
    return HttpResponse(one)