from django.contrib.auth.models import User
from rest_framework import serializers

from tag.models import Tag

from .models import Recipe


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'title', 'category', 'author', 'preparation', 'servings',
                  'description', 'public', 'tags', 'tag_objects', 'tag_links']
    public = serializers.BooleanField(source='is_published', read_only=True)
    preparation = serializers.SerializerMethodField(read_only=True)
    servings = serializers.SerializerMethodField(read_only=True)
    category = serializers.StringRelatedField(read_only=True)
    tag_objects = TagSerializer(many=True, source='tags', read_only=True)
    tag_links = serializers.HyperlinkedRelatedField(
        many=True,
        source='tags',
        view_name='recipes:recipes_api_v2_tag',
        read_only=True,
    )

    def get_preparation(self, recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'

    def get_servings(self, recipe):
        return f'{recipe.servings} {recipe.servings_unit}'
