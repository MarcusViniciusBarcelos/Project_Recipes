from unittest.mock import patch

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import RecipeBaseFunctionalTest


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    @patch('recipes.views.site.PER_PAGE', new=2)
    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, "body")
        self.assertIn('Nenhuma receita encontrada', body.text)

    @patch('recipes.views.site.PER_PAGE', new=2)
    def test_recipe_search_input_can_find_correct_recipes(self):
        recipes = self.make_recipe_in_batch()

        title_needed = 'This is what I need'

        recipes[0].title = title_needed
        recipes[0].save()

        # usuario abre a pagina
        self.browser.get(self.live_server_url)

        # ve um campo de busca com o texto "Search for a recipe..."
        search_input = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Search for a recipe..."]'
        )

        # clica nesse input e digita o termo de busca
        #  para encontrar a receita com o titulo desejado

        search_input.send_keys(title_needed)
        search_input.send_keys(Keys.ENTER)

        # usuario vê o que estava procurando na pagina
        self.assertIn(
            title_needed,
            self.browser.find_element(By.CLASS_NAME, 'main-content-list').text
        )

    @patch('recipes.views.site.PER_PAGE', new=2)
    def test_recipe_home_page_pagination(self):
        self.make_recipe_in_batch(8)

        # usuario abre a pagina
        self.browser.get(self.live_server_url)

        # Vê que tem uma paginação e clica na pagina 2
        page2 = self.browser.find_element(
            By.XPATH,
            '//a[@aria-label="Go to page 2"]'
        )
        page2.click()
        # Vê que tem mais duas receitas na pagina 2
        self.assertEqual(
            len(self.browser.find_elements(By.CLASS_NAME, 'recipe')),
            2
        )
