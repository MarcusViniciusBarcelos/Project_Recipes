from collections import defaultdict

from django.contrib.auth.models import User
from django.db import models
from django.forms import ValidationError
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from tag.models import Tag


class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=65, verbose_name=_('title'))
    description = models.CharField(
        max_length=165,
        verbose_name=_('description')
    )
    slug = models.SlugField(unique=True, verbose_name=_('slug'))
    preparation_time = models.IntegerField(verbose_name=_('preparation time'))
    preparation_time_unit = models.CharField(
        max_length=65,
        verbose_name=_('preparation time unit')
    )
    servings = models.IntegerField(verbose_name=_('servings'))
    servings_unit = models.CharField(
        max_length=65,
        verbose_name=_('servings unit')
    )
    preparation_steps = models.TextField(verbose_name=_('preparation steps'))
    preparation_steps_is_html = models.BooleanField(
        default=False,
        verbose_name=_('preparation steps is html')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created at')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('updated at')
    )
    is_published = models.BooleanField(
        default=False, verbose_name=_('is published'))
    cover = models.ImageField(
        upload_to='recipes/cover/%Y/%m/%d/',
        blank=True, default='',
        verbose_name=_('cover')
    )

    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, default=None, verbose_name=_('category'))
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, default=None, verbose_name=_('author'))
    tags = models.ManyToManyField(
        Tag, blank=True, default='', verbose_name=_('tags'))

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("recipes:recipe", args=((self.id,)))

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.title)}'
            self.slug = slug
        return super().save(*args, **kwargs)

    def clean(self, *args, **kwargs):
        error_messages = defaultdict(list)

        recipe_from_db = Recipe.objects.filter(
            title_iexact=self.title
        ).first()

        if recipe_from_db:
            if recipe_from_db.pk != self.pk:
                error_messages['title'].append(
                    'Found recipes with the same title'
                )

        if error_messages:
            raise ValidationError(error_messages)
