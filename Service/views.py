from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from newspaper import Article
from bs4 import BeautifulSoup
from gensim.summarization import summarize
from collections import OrderedDict
import json,  requests, regex

# Custom Functions


# def replaceAll(str_):
#     str_ = str_.split('\n')
#     str_ = ' '.join(str_)
#     return str_
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
    return HttpResponse("OK")