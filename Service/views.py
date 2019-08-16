from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from newspaper import Article
import json

# Create your views here.
def index(request):
    return HttpResponse("Hello World!!")

def check_health(request):
    return HttpResponse("OK")  # 서버 정상 작동 중

@csrf_exempt
def articlecomp_action_keyword(request):
    text = request.body.decode('utf-8')
    print(text)

    return HttpResponse("NO")

@csrf_exempt
def articlecomp_action_now(request):
    text = request.body.decode('utf-8')
    print(text)

    json_data = json.loads(text)
    return HttpResponse("OK")
