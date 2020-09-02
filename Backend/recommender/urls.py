from django.urls import path
from . import views

app_name = 'recommender'

urlpatterns = [
    path('<int:pk>/',views.recommend,name='reco')
]