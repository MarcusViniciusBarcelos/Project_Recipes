

from django.db import models


class Questions(models.Model):
    title = models.CharField(max_length=250)
    answer = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Rules(models.Model):
    name = models.CharField(max_length=150)
    questions = models.ManyToManyField(Questions, blank=True, default=None, )
    result = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class RulesQuestions(models.Model):
    rule = models.ForeignKey(Rules, on_delete=models.CASCADE)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)

    def __str__(self):
        return self.rule.name + ' - ' + self.question.title
