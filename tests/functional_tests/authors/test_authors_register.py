import pytest
from parameterized import parameterized
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import AuthorsBaseTest


@pytest.mark.functional_test
class AuthorRegisterTest(AuthorsBaseTest):

    def fill_form_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, 'input')

        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 20)

    def get_form(self):
        return self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form'
        )

    def form_field_test_with_callback(self, callback):
        # usuario abre a pagina de registro
        self.browser.get(self.live_server_url + '/authors/register/')

        # ve um formulario com campos de cadastro
        form = self.get_form()

        # preenche os campos com apenas um espaço em branco
        self.fill_form_dummy_data(form)

        # preenche o campo email com um email valido
        form.find_element(By.NAME, 'email').send_keys('email@gmail.com')
        callback(form)
        return form

    @parameterized.expand([
        ('username', 'This field must not be empty'),
        ('last_name', 'write your last name'),
        ('first_name', 'write your first name'),
        ('password', 'Password must not be empty'),
        ('password2', 'This field must not be empty'),
    ])
    def test_empty_current_error_message(self, field, msg):
        def callback(form):
            # reescreve o campo atual com um espaço em branco
            current_field = form.find_element(By.NAME, field)
            current_field.send_keys(' ')

            # envia o formulario
            current_field.send_keys(Keys.ENTER)

            # vê os erros de preenchimento do formulario
            form = self.get_form()
            # olha para o erro de preenchimento do campo atual
            self.assertIn(msg, form.text)
        self.form_field_test_with_callback(callback)

    def test_user_valid_data_register_successfuly(self):
        # usuario abre a pagina de registro
        self.browser.get(self.live_server_url + '/authors/register/')

        # ve um formulario com campos de cadastro
        form = self.get_form()

        # preenche o formulario corretamente
        form.find_element(By.NAME, 'username').send_keys('username')
        form.find_element(By.NAME, 'first_name').send_keys('first_name')
        form.find_element(By.NAME, 'last_name').send_keys('last_name')
        form.find_element(By.NAME, 'email').send_keys('email@gmail.com')
        form.find_element(By.NAME, 'password').send_keys('Teste123@')
        form.find_element(By.NAME, 'password2').send_keys('Teste123@')

        # envia o formulario
        form.submit()

        # Vê a mensagem de sucesso ao criar usuario
        self.assertIn(
            'Your user is created successfully, please log in',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
