from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.

class user_urls(models.Model):
    title = models.CharField(default='No Title', max_length=10)
    url_date = models.DateTimeField(blank=False)
    original_url = models.URLField(blank=False)
    short_char = models.CharField(blank=True, max_length=10)
    visits = models.IntegerField(default=0)
    expiry = models.DateTimeField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.title)

class public_urls(models.Model):
    url_date = models.DateTimeField(blank=False)
    original_url = models.URLField(blank=False)
    short_char = models.CharField(blank=True, max_length=6)
    visits = models.IntegerField(default=0)
    expiry = models.DateTimeField(blank=True)

    def __str__(self):
        return str(self.url_date)