from django.contrib import admin
from .models import Article,UserFile,UserLog,Tfidf
# Register your models here.

admin.site.register(Article)
admin.site.register(UserFile)
admin.site.register(Tfidf)
admin.site.register(UserLog)