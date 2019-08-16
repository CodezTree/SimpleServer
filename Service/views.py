from django.shortcuts import render
from django.http import HttpResponse
from newspaper import Article
import json

# Create your views here.
def index(request):
    return HttpResponse("Hello World!!")

def check_health(request):
    return HttpResponse("OK")  # 서버 정상 작동 중

def articlecomp_action_keyword(request):
    return HttpResponse("NO")

def articlecomp_action_now(request):
    text = request.body.decode('utf-8')
    print(text)

    json_data = json.load(text)
    return HttpResponse("OK")
