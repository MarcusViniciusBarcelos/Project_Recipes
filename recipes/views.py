import os

from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView

from utils.pagination import make_pagination

from .models import Recipe

PER_PAGE = int(os.environ.get('PER_PAGE', 9))


class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = 'recipes'
    paginate_by = None
    ordering = ['-id']
    template_name = 'recipes/pages/home.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(
            is_published=True,
        )
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            self.request,
            context.get('recipes'),
            PER_PAGE
        )
        context.update(
            {
                'recipes': page_obj,
                'pagination_range': pagination_range
            }
        )

        return context


class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'


class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(
            category__id=self.kwargs.get('category_id'),
            is_published=True
        ).order_by('-id')

        if not queryset:
            raise Http404()

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update({
            'title': f'{context.get("recipes")[0].category.name} - Category',
        })

        return context


class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'

    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '')
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(
            Q(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term)
            )
        ).order_by('-id')

        if not queryset:
            raise Http404()

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('q', '')
        context.update({
            'page_title': f'search for "{ search_term }" |',
            'search_term': search_term,
            'additional_url_query': f'&q={ search_term }',
        })

        return context


def recipe(request, id):
    recipe = get_object_or_404(Recipe, pk=id, is_published=True)
    return render(request, 'recipes/pages/recipe-view.html', {
        'recipe': recipe,
        'is_detail_page': True,
    })
