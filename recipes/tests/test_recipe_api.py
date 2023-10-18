from os import access
from unittest.mock import patch
from urllib import response

from django.urls import reverse
from rest_framework import test

from recipes.tests.test_recipe_base import RecipeMixin


class RecipeAPIv2TestMixin(RecipeMixin):
    def get_recipe_list_reverse_url(self, reverse_result=None):
        api_url = reverse_result or reverse('recipes:recipes-api-list')
        return api_url

    def get_recipe_api_list(self, reverse_result=None):
        api_url = self.get_recipe_list_reverse_url(reverse_result)
        response = self.client.get(api_url)  # type: ignore
        return response

    def get_auth_data(self, username='testuser', password='testpassword'):
        userdata = {
            'username': username,
            'password': password
        }
        user = self.make_author(
            username=userdata['username'],
            password=userdata['password']
        )
        response = self.client.post(  # type: ignore
            reverse('recipes:token_obtain_pair'),
            data={**userdata}
        )
        return {
            'jwt_access_token': response.data.get('access'),
            'jwt_refresh_token': response.data.get('refresh'),
            'user': user,
        }

    def get_recipe_raw_data(self):
        return {
            'title': 'Recipe title',
            'description': 'Recipe description',
            'preparation_time': 30,
            'preparation_time_unit': 'minutes',
            'servings': 4,
            'servings_unit': 'people',
            'preparation_steps': 'Recipe preparation steps'
        }


class RecipeAPIv2Test(test.APITestCase, RecipeAPIv2TestMixin):
    def test_recipe_api_list_returns_status_code_200(self):
        self.get_auth_data()
        response = self.get_recipe_api_list()
        self.assertEqual(200, response.status_code)

    @patch('recipes.views.api.RecipeAPIV2Pagination.page_size', new=7)
    def test_recipe_api_list_loads_correct_number_of_recipes(self):
        wanted_number_of_recipes = 7
        self.make_recipe_in_batch(qtd=wanted_number_of_recipes)
        response = self.client.get(reverse('recipes:recipes-api-list'))
        qtd_of_loaded_recipes = len(
            response.data.get('results')  # type: ignore
        )
        self.assertEqual(
            wanted_number_of_recipes,
            qtd_of_loaded_recipes
        )

    def test_recipe_api_list_do_not_show_not_published_recipes(self):
        recipes = self.make_recipe_in_batch(qtd=2)
        recipe_not_published = recipes[0]
        recipe_not_published.is_published = False
        recipe_not_published.save()
        response = self.get_recipe_api_list()
        self.assertEqual(1, len(response.data.get('results')))  # type: ignore

    @patch('recipes.views.api.RecipeAPIV2Pagination.page_size', new=10)
    def test_recipe_api_list_loads_recipes_by_category_id(self):
        # Creates categories
        category_wanted = self.make_category(name='WANTED_CATEGORY')
        category_not_wanted = self.make_category(name='NOT_WANTED_CATEGORY')

        # Creates 10 recipes
        recipes = self.make_recipe_in_batch(qtd=10)

        # Change all recipes to the wanted category
        for recipe in recipes:
            recipe.category = category_wanted
            recipe.save()

        # Change one recipe to the NOT wanted category
        # As a result, this recipe should NOT show in the page
        recipes[0].category = category_not_wanted
        recipes[0].save()

        # Action: get recipes by wanted category_id
        api_url = reverse('recipes:recipes-api-list') + \
            f'?category_id={category_wanted.pk}'
        response = self.get_recipe_api_list(reverse_result=api_url)

        # We should only see recipes from the wanted category
        self.assertEqual(9, len(response.data.get('results')))  # type: ignore

    def test_recipe_api_list_user_must_send_jwt_ttoken_to_create_recipe(self):
        api_url = self.get_recipe_list_reverse_url()
        response = self.client.post(api_url, {})
        self.assertEqual(401, response.status_code)

    def test_recipe_api_list_logged_user_can_create_a_recipe(self):
        recipe_raw_data = self.get_recipe_raw_data()
        auth_data = self.get_auth_data()
        jwt_access_token = auth_data.get('jwt_access_token')
        response = self.client.post(
            self.get_recipe_list_reverse_url(),
            data=recipe_raw_data,
            HTTP_AUTHORIZATION=f'Bearer {jwt_access_token}'
        )
        self.assertEqual(
            response.status_code, 201
        )

    def test_recipe_api_list_logged_user_can_update_a_recipe(self):
        # Arange (config do teste)
        recipe = self.make_recipe()
        access_data = self.get_auth_data(username='testuser2')
        jwt_access_token = access_data.get('jwt_access_token')
        author = access_data.get('user')
        recipe.author = author
        recipe.save()
        wanted_new_title = f'New title updated by {author.username}' if author else 'New title'

        # Act (executa o teste)
        response = self.client.patch(
            reverse('recipes:recipes-api-detail', args=[recipe.pk]),
            data={
                'title': wanted_new_title
            },
            HTTP_AUTHORIZATION=f'Bearer {jwt_access_token}'
        )

        # Assert (verifica se o teste passou)
        self.assertEqual(
            response.data.get('title'), wanted_new_title  # type: ignore
        )

    def test_recipe_api_list_logged_user_can_update_a_recipe_owned_by_another_user(self):
        # Arange (config do teste)
        recipe = self.make_recipe()

        # this is the actual owner of the recipe
        access_data = self.get_auth_data(username='testuser2')
        author = access_data.get('user')
        recipe.author = author
        recipe.save()

        # this user cannot update the recipe because he is not the owner
        another_user = self.get_auth_data(username='another_user')

        # Act (executa o teste)
        # this patch request is made by another_user
        response = self.client.patch(
            reverse('recipes:recipes-api-detail', args=[recipe.pk]),
            data={},
            HTTP_AUTHORIZATION=f'Bearer {another_user.get("jwt_access_token")}'
        )

        # Assert (verifica se o teste passou)
        # Another user cannot update the recipe, so the response should be 403 Forbidden
        self.assertEqual(
            response.status_code, 403
        )
