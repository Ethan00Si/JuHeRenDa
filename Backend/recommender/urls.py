from django.urls import path
from . import views

app_name = 'recommender'

urlpatterns = [
    path('',views.recommend,name='recommend'),
    # path('<int:user_id>/', views.detail, name='detail')
    path('<int:user_id>/', views.recommend_news, name='recommend_news')
]