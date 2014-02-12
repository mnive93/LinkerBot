from django.db import models
from django.contrib.auth.models import User
class TopicsManager(models.Manager):
    def user_topic_follow(self, user, topic):
        foll_list = self.topic_followers(topic)
        if user in foll_list:
            return True
        return False
class Genre(models.Model):
    title = models.CharField(max_length=100)
    identifier = models.CharField(max_length = 100)
    user = models.ManyToManyField(User,related_name = "genretouser")
    def __unicode__(self):
       return self.title

