from django.urls import path
from . import views

app_name = 'recommender'

urlpatterns = [
    path('',views.recommend,name='recommend'),
    path('<int:pk>/',views.detail,name='detail')
]