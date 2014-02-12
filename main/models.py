from django.db import models
from authentication.models import Genre
from django.contrib.auth.models import User
# Create your models here.
class Links(models.Model):
    title = models.CharField(max_length=500)
    content = models.CharField(max_length =500 )
    url = models.CharField(max_length=100)
    genre = models.ForeignKey(Genre,related_name = 'genre')
    user = models.ForeignKey(User,related_name='user')
    img_src = models.CharField(max_length=200)
    posted_time = models.DateTimeField(auto_now = True)




