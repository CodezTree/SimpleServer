from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from newspaper import Article
from bs4 import BeautifulSoup
from gensim.summarization import summarize
from collections import OrderedDict
import json, requests, regex, random
from .models import User


# Custom Functions


def replaceAll(str_):
    str_ = str_.split('\n')
    str_ = ' '.join(str_)
    return str_


# def getURL(page):
#     start_link = page.find("a href")
#     if start_link == -1:
#         return None, 0
#     start_quote = page.find('"', start_link)
#     end_quote = page.find('"', start_quote + 1)
#     url = page[start_quote + 1: end_quote]
#     return url, end_quote
#
# def get_text(URL):
#     html_src = requests.get(URL)
#     soup = BeautifulSoup(html_src.text, 'lxml')
#     text = ''
#     for item in soup.find_all("div", id="articleBodyContents"):
#         text = text + str(item.find_all(text=True))
#         return clean_text(text)
#
# # 결과 정보에 대해 특수문자 제거 등 텍스트를 정리한다.
# def clean_text(text):
#     cleanText = regex.sub("[a-zA-Z]", "", text)
#     cleanText = regex.sub("[\{\}\[\]\/?;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]", "", cleanText)
#     return cleanText


# Create your views here.


def index(request):
    return HttpResponse("Hello World!!")


def check_health(request):
    return HttpResponse("OK")  # 서버 정상 작동 중


@csrf_exempt
def register(request):
    text = request.body.decode('utf-8')

    json_data = json.loads(text)
    access_token = json_data['context']['session']['accessToken']
    print(access_token)
    flag = True  # if True -> OK

    try:
        User.objects.get(user_token=access_token)
    except:
        flag = False

    response_data = OrderedDict()
    temp_num = str(random.randrange(0, 9999)).zfill(4)

    response_data['version'] = json_data['version']

    if not flag:
        response_data['resultCode'] = "ec_user_exists"
        response_data['output'] = {'reg_num': ''}
    else:
        new_user = User(user_token=access_token, temp_num=temp_num)
        new_user.save()  # Add Temp

        response_data['resultCode'] = "OK"
        response_data['output'] = {'reg_num': temp_num}

    response = json.dumps(response_data, ensure_ascii=False, indent='\t')

    return HttpResponse(response, content_type='application/json')


@csrf_exempt
def register_check(request):
    text = request.body.decode('utf-8')

    json_data = json.loads(text)
    access_token = json_data['context']['session']['accessToken']
    print(access_token)

    response_data = OrderedDict()
    check = ''
    response_data['version'] = json_data['version']
    response_data['resultCode'] = "OK"

    if User.objects.get(user_token=access_token).firebase_token != None:
        check = 'done'
    else:
        check = 'failed'

    response_data['output'] = {'reg_num': '', 'check': check}

    response = json.dumps(response_data, ensure_ascii=False, indent='\t')

    return HttpResponse(response, content_type='application/json')


@csrf_exempt
def register_app_check(request):
    if request.method == 'POST':
        user_token = ""
        reg_check_num = str(request.POST['check_num'])
        firebase_token = str(request.POST['firebase_token'])

        try:
            u = User.objects.get(temp_num=reg_check_num)
            u.temp_num = ""
            u.firebase_token = firebase_token
            user_token = str(u.user_token)
            u.save()
        except:
            return HttpResponse("FAILED")  # Compare Failed

        return HttpResponse("FINISH$"+user_token)

    return HttpResponse("POSTFAILED")



@csrf_exempt
def articlecomp_action_keyword(request):
    text = request.body.decode('utf-8')

    json_data = json.loads(text)
    keyword = json_data['action']['parameters']['keyword']['value']
    summarized = ''
    print('keyword :', keyword)

    new_url = str('https://news.google.com/search?q=' + keyword + '&hl=ko&gl=KR&ceid=KR%3Ako')

    # new_url = new_url[2:-2]
    print(new_url)
    resp = requests.get(new_url)
    soup = BeautifulSoup(resp.text, 'lxml')

    items = soup.select('div > div > article > a')

    titles = []
    links = []
    for item in items:
        title = item.text
        link = 'https://news.google.com' + item.get('href')[1:]
        titles.append(title)
        links.append(link)

    a = Article(links[0], language='ko')

    a.download()
    a.parse()

    article_text = str(a.text)

    article_text = replaceAll(article_text)

    print(article_text)

    summarized = summarize(article_text, ratio=0.3, split=True)[:3]
    summarized_ = ' '.join(summarized)
    print(summarized_)

    response_data = OrderedDict()

    response_data['version'] = json_data['version']
    response_data['resultCode'] = "OK"
    response_data['output'] = {'summarized': summarized_, 'keyword': keyword}

    response = json.dumps(response_data, ensure_ascii=False, indent='\t')

    print(response)

    return HttpResponse(response, content_type='application/json')


@csrf_exempt
def articlecomp_action_now(request):
    text = request.body.decode('utf-8')
    print(text)

    json_data = json.loads(text)

    response_data = OrderedDict()

    response_data['version'] = json_data['version']
    response_data['resultCode'] = "OK"
    response_data['output'] = {'summarized_now': ''}

    response = json.dumps(response_data, ensure_ascii=False, indent='\t')
    return HttpResponse(response, content_type='application/json')


@csrf_exempt
def articlecomp_action_keyword_send_app(request):
    text = request.body.decode('utf-8')

    json_data = json.loads(text)
    keyword = json_data['action']['parameters']['keyword']['value']

    response_data = OrderedDict()

    response_data['version'] = json_data['version']
    response_data['resultCode'] = "OK"
    response_data['output'] = {'summarized': '', 'keyword': keyword}

    response = json.dumps(response_data, ensure_ascii=False, indent='\t')
    return HttpResponse(response, content_type='application/json')


@csrf_exempt
def url_share_app(request):
    if request.method == 'POST':
        user_token = request.POST['user_token']
        url_str = request.POST['url_str']

        a = Article(url_str, language='ko')

        a.download()
        a.parse()

        article_text = str(a.text)

        article_text = replaceAll(article_text)

        summarized = summarize(article_text, ratio=0.3, split=True)[:3]
        summarized_ = ' '.join(summarized)

        temp_list = [{'summarized': summarized_, 'link': url_str}]

        json_arr = json.dumps(temp_list, ensure_ascii=False, indent='\t')

        u = User.objects.get(user_token=user_token)
        u.user_sum_temp = json_arr
        u.save()  # Temporary Saving

        return HttpResponse("OK")


@csrf_exempt
def url_quit(request):
    json_data = json.loads(request)
    user_token = json_data["context"]["session"]["accessToken"]

    u = User.objects.get(user_token=user_token)
    u.user_sum_temp = ""
    u.save()  # erase Data

    response_data = OrderedDict()

    response_data['version'] = json_data['version']
    response_data['resultCode'] = "OK"
    response_data['output'] = {'summarized_now': ''}

    response = json.dumps(response_data, ensure_ascii=False, indent='\t')
    return HttpResponse(response, content_type='application/json')


@csrf_exempt
def url_done(request):
    json_data = json.loads(request)
    user_token = json_data["context"]["session"]["accessToken"]

    u = User.objects.get(user_token=user_token)
    sum_temp = json.dumps(u.user_sum_temp)

    response_data = OrderedDict()

    response_data['version'] = json_data['version']
    response_data['resultCode'] = "OK"
    response_data['output'] = {'summarized_now': sum_temp["summarized"]}

    response = json.dumps(response_data, ensure_ascii=False, indent='\t')
    return HttpResponse(response, content_type='application/json')


@csrf_exempt
def url_reject(request): # same url quit
    json_data = json.loads(request)
    user_token = json_data["context"]["session"]["accessToken"]

    u = User.objects.get(user_token=user_token)
    u.user_sum_temp = ""
    u.save()  # erase Data

    response_data = OrderedDict()

    response_data['version'] = json_data['version']
    response_data['resultCode'] = "OK"
    response_data['output'] = {'summarized_now': ''}

    response = json.dumps(response_data, ensure_ascii=False, indent='\t')
    return HttpResponse(response, content_type='application/json')


@csrf_exempt
def url_confirm(request):
    json_data = json.loads(request)
    user_token = json_data["context"]["session"]["accessToken"]

    u = User.objects.get(user_token=user_token)
    sum_temp = json.dumps(u.user_sum_temp)

    firebase_token = u.firebase_token
    summarized = sum_temp['summarized']
    link = sum_temp['link']

    u.user_sum_temp = ""
    u.save()  # erase Data

    url = "https://fcm.googleapis.com/fcm/send"
    headers = {'Content-Type': 'application/json; UTF-8',
               'Authorization': 'key=AAAAGDcH1Ds:APA91bEtAp_DCsG9seg46HITANxNuREbOntSYz3YZ0YeniNscdJrlF9KwnX2rsHf-AKJDqCUq9u_TG9zpKg-rhZdT1-_6nVW-l5ym9f-kRo0UguO5fssvTSnqPK0C69gn5McyrZSM96F'}
    body = '''{
                "to":"'''+firebase_token+'''"
                "notification": {
                    "title": "세줄요약",
                    "body": "요약 결과가 전송되었습니다."
                },
                "data": {
                    "data_list": [{"'''+summarized+'": "'+link+'''"}]
                }
              }'''

    requests.post(url=url, headers=headers, data=body.encode('utf-8'))

    # response
    response_data = OrderedDict()

    response_data['version'] = json_data['version']
    response_data['resultCode'] = "OK"
    response_data['output'] = {'summarized_now': ''}

    response = json.dumps(response_data, ensure_ascii=False, indent='\t')
    return HttpResponse(response, content_type='application/json')


def note(request):
    return render(request, 'save.html')