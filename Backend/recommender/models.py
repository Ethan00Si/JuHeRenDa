from django.db import models

# Create your models here.
class Article(models.Model):
    art_id = models.AutoField(primary_key=True)
    art_source = models.CharField(max_length=32, blank=True, null=True)
    art_url = models.CharField(max_length=255, blank=True, null=True)
    art_title = models.CharField(max_length=255, blank=True, null=True)
    art_content = models.TextField(blank=True, null=True)
    art_type = models.CharField(max_length=32, blank=True, null=True)
    art_image = models.CharField(max_length=255, blank=True, null=True)
    art_time = models.DateTimeField(blank=True, null=True)
    art_legal = models.IntegerField(blank=True, null=True)
    entity_id = models.CharField(max_length=255, blank=True, null=True)
    entity_idx = models.CharField(max_length=255, blank=True, null=True)
    relation_id = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'article'


class Tfidf(models.Model):
    word_id = models.AutoField(primary_key=True)
    word = models.CharField(max_length=32, blank=True, null=True)
    word_idf = models.FloatField(blank=True, null=True)
    word_col = models.PositiveIntegerField(unique=True, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tfidf'


class UserFile(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=64, blank=True, null=True)
    user_number = models.CharField(unique=True, max_length=16, blank=True, null=True)
    user_gender = models.IntegerField(blank=True, null=True)
    user_tags = models.CharField(max_length=255, blank=True, null=True)
    user_create_time = models.DateTimeField(blank=True, null=True)
    user_last_login_time = models.DateTimeField(blank=True, null=True)
    user_legal = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'user_file'


class UserLog(models.Model):
    log_id = models.AutoField(primary_key=True)
    user_id = models.PositiveIntegerField(blank=True, null=True)
    behavior = models.IntegerField(blank=True, null=True)
    behavior_time = models.DateTimeField(blank=True, null=True)
    art_id = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'user_log'