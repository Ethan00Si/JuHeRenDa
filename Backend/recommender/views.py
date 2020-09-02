from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.utils import timezone
from .models import Article,UserLog,UserFile,Tfidf
# Create your views here.
def recommend(request):
    '''
        Recommender code
    '''

    return HttpResponse("推荐算法")

def detail(request,pk):
    
    # 通过primary key在数据库中查找指定文章
    # get方法只能返回一个数据项
    # article = Article.objects.get(pk=pk)

    # 通过sql语句查询
    # 如果传入参数，不要用format，而是在raw方法的第二个参数的位置传入参数列表
    # 返回的是一个列表，注意索引
    article = Article.objects.raw('SELECT * FROM article WHERE art_id = %s',[pk])[0]
    
    # 获取属性,也可以把整个article object返回前端，在前端获取对应属性
    # art_url = article.art_url
    # art_title = article.art_title
    # art_source = article.art_source
    # art_img = article.art_image

    # filter方法可以返回一个数据集，这里查找所有source为ai的新闻
    # articles = Article.objects.filter(art_source='ai.ruc.edu.cn')

    # 同样可以通过raw方法使用sql语句查询
    # 支持各种sql语句，AS什么的，这里同样查找source为ai的新闻集合，但限制了10个返回值，不会查完整个数据库
    articles = Article.objects.raw('SELECT * FROM article WHERE art_source = %s LIMIT 10',['ai.ruc.edu.cn'])
    
    # 通过单词查找指定的Tfidf矩阵，这里忘记了tfidf的格式，意思是这个意思
    # 因为数据库中还没存tfidf，所以查询不到会报错
    # word = 'test'
    # tfidf = Tfidf.objects.get(word=word)

    # 通过用户的注册日期查找一批用户
    # 因为数据库中还没有用户数据，所以查询不到会报错
    # users = UserFile.objects.filter(user_create_time__lte = timezone.localtime())


    # 将值传到前端
    context = {
        'article':article,
        'articles':articles,
        #'users':users,          
        #'tfidf':tfidf
    }

    # 网站默认解析Httpresponse，利用render生成，这里用网站调试（因为我还没看微信小程序）
    return render(request,'recommender/layout.html',context=context)
    
    # 微信小程序默认解析json
    # return JsonResponse(data=context)
