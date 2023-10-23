from django.db import models


class Variables(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Values(models.Model):
    name = models.CharField(max_length=50)

    variables = models.ForeignKey(
        Variables, on_delete=models.SET_NULL, null=True, blank=True, default=None,)

    def __str__(self):
        return self.name


class Rules(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    variable = models.ManyToManyField(Variables, blank=True, default=None, )

    def __str__(self):
        return self.name
