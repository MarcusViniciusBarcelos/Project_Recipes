from unittest import TestCase

from django.http import HttpRequest
from django.urls import reverse

from recipes.models import Recipe
from recipes.tests.test_recipe_base import RecipeTestBase
from utils.pagination import make_pagination, make_pagination_range


class PaginationTest(RecipeTestBase):
    def test_make_pagination_range_returns_a_pagination_range(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1,
        )['pagination']

        self.assertEqual([1, 2, 3, 4], pagination)

    def test_first_range_is_static_if_current_page_is_less_than_middle_page(self):

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=5,
        )['pagination']
        self.assertEqual([4, 5, 6, 7], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1,
        )['pagination']

        self.assertEqual([1, 2, 3, 4], pagination)

    def test_make_sure_middle_ranges_are_correct(self):

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=5,
        )['pagination']
        self.assertEqual([4, 5, 6, 7], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=4,
        )['pagination']

        self.assertEqual([3, 4, 5, 6], pagination)

    def test_make_pagination_range_is_static_when_last_page_is_next(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=20,
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)

    def test_pagination_range_start_and_stop(self):
        page_range = list(range(1, 21))
        qty_pages = 6
        current_page = 1  # Simulate a current page close to the start
        pagination = make_pagination_range(
            page_range, qty_pages, current_page)['pagination']
        self.assertEqual([1, 2, 3, 4, 5, 6], pagination)

        current_page = 18  # Simulate a current page close to the end
        pagination = make_pagination_range(
            page_range, qty_pages, current_page)['pagination']
        self.assertEqual([15, 16, 17, 18, 19, 20], pagination)

    def test_invalid_current_page(self):
        for _ in range(30):
            self.make_recipe(
                slug=f'test-pagination-{_}',
                author_data={
                    'username': {_}
                }
            )
        request = HttpRequest()
        request.GET['page'] = 'invalid'  # Simulate an invalid page value
        queryset = Recipe.objects.all()  # Provide a valid queryset
        per_page = 10
        page_obj, pagination_range = make_pagination(
            request, queryset, per_page)
        self.assertEqual(page_obj.number, 1)  # Expect the default current page

    def test_pagination_loads_recipes(self):
        # need a recipe for this test
        for _ in range(30):
            recipe = self.make_recipe(
                slug=f'test-pagination-{_}',
                author_data={
                    'username': {_}
                }
            )
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=20,
        )['pagination']

        response = self.client.get(reverse('recipes:home'))
        response_context_recipes = response.context['recipes']
        expected_recipes_count = 9
        self.assertEqual(len(response_context_recipes), expected_recipes_count)
