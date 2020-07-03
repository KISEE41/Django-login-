from django.db import models
from django.utils import timezone

class Comment(models.Model):
    name = models.CharField(max_length=50)
    text = models.TextField()
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '(Name: {}, Date_of_creation: {})'.format(self.name, self.date_added)