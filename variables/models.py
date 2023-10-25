
from django.db import models


class Questions(models.Model):
    title = models.CharField(max_length=250)
    answer = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Rules(models.Model):
    name = models.CharField(max_length=50)
    questions = models.ManyToManyField(Questions, blank=True, default=None, )
    result = models.CharField(max_length=50)

    def __str__(self):
        return self.name
