import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By

from .base import AuthorsBaseTest


@pytest.mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):
    def test_user_valid_data_can_login_successfully(self):
        string_password = 'pass'
        user = User.objects.create_user(
            username='my_user', password=string_password)

        # usuario abre a pagina de login
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # usuario vê o formulario de login
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_field = self.browser.find_element(By.NAME, 'username')
        password_field = self.browser.find_element(By.NAME, 'password')

        # usuario digita seu usuário e senha
        username_field.send_keys(user.username)
        password_field.send_keys(string_password)

        # usuario envia o formulario de login
        form.submit()

        # usuario vê a mensagem de login com sucesso e seu usuário
        self.assertIn(
            f'You are logged in with { user.username }.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
