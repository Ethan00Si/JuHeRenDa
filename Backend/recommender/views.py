from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.utils import timezone
from .models import Article,UserLog,UserFile,Tfidf
from .CB import refresh_news
from datetime import datetime
import numpy
# from py2neo import Graph,Node,Relationship,Subgraph

graph = Graph('bolt://localhost:7687',username='neo4j',password='123')

# Create your views here.
def recommend(request):
    '''
        Recommender code
    '''
    data = numpy.random.randn(100,100,100,100)
    return render(request,'recommender/layout.html',{'data':data})

def entity_yield(article):
    if not article.entity_id:
        title = []
        title.append({'content':article.art_title,'isLight':0})
        article.art_title = title
        return

    entities = []
    pre_end = 0
    title = []
    _title = article.art_title
    for eid in article.entity_id.split(','):
        node = graph.nodes.match(id=int(eid)).first()
        # 删除id
        del node['id']
        entities.append(node)

    for eidx in article.entity_idx.split(','):
        span = eidx.split(':')
        start = int(span[0])
        end = int(span[1])

        title.append({'content':_title[pre_end:start],'isLight':0})
        title.append({'content':_title[start:end],'isLight':1})
        pre_end = end
    title.append({'content':_title[pre_end:],'isLight':0})

    article.entities = entities
    article.art_title = title


def recommend_news(request, user_id):
    """
    user_id 是用户id，对应数据库中的id
    """
    # ret_news_id 是要返回的新闻数据库中对应的id
    ret_news_id = refresh_news.refresh_news(user_id)
    ret_news_id = [1,2,3,4,5,6,7,8,9,10]

    articles_list = list()

    articles = Article.objects.raw('SELECT * FROM article WHERE entity_id != \'\'')
    for item in ret_news_id:
        article = articles[item]
        entity_yield(article)
        tmp = dict()
        tmp['newsID'] = article.art_id
        tmp['title'] = article.art_title
        tmp['publish_date'] = datetime.date(article.art_time)
        tmp['source'] = article.art_source
        tmp['url'] = article.art_url
        tmp['entity'] = article.entities
        print(article.entities)
        articles_list.append(tmp)

    return JsonResponse(articles_list, safe=False)
    #return render(request,'recommender/layout.html',{'list':articles_list})
