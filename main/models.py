from django.db import models
from authentication.models import Genre
from django.contrib.auth.models import User
from decimal import *
# Create your models here.
class Links(models.Model):
    title = models.TextField()
    content = models.TextField()
    url = models.TextField()
    genre = models.ForeignKey(Genre,related_name = 'genre')
    user = models.ForeignKey(User,related_name='user')
    img_src = models.CharField(max_length=200)
    posted_time = models.DateTimeField(auto_now = True)
class Clusters(models.Model):
    link = models.ForeignKey(Links,related_name = 'link')
    distance_metric = models.DecimalField(max_digits=7, decimal_places=5,
                   default=Decimal('0.00000'))





