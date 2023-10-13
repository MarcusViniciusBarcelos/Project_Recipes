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
            f'Você está logado com { user.username }.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_login_create_raises_404_if_not_POST_method(self):
        self.browser.get(
            self.live_server_url +
            reverse('authors:login_create')
        )

        self.assertIn(
            'Not Found',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_form_message_invalid_username_or_password(self):
        # usuario abre a pagina de login
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # usuario vê o formulario de login
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        # tenta enviar valores vazios
        username_field = form.find_element(
            By.NAME, 'username').send_keys(' ')
        password_field = form.find_element(
            By.NAME, 'password').send_keys(' ')

        # usuario envia o formulario de login
        form.submit()

        # vê uma mensagem de erro na tela
        self.assertIn(
            'Invalid username or password',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_form_message_invalid_credentials(self):
        # usuario abre a pagina de login
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # usuario vê o formulario de login
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        # tenta enviar usuario certo e a senha vazia
        username_field = form.find_element(
            By.NAME, 'username').send_keys('marcus')
        password_field = form.find_element(
            By.NAME, 'password').send_keys('testandodododo')

        # usuario envia o formulario de login
        form.submit()

        # vê uma mensagem de erro na tela
        self.assertIn(
            'Invalid credentials',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
