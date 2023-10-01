from parameterized import parameterized
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import AuthorsBaseTest


class AuthorRegisterTest(AuthorsBaseTest):
    def get_by_placeholder(self, web_element, placeholder):
        return web_element.find_element(
            By.XPATH, f'//input[@placeholder="{ placeholder }"]'
        )

    def fill_form_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, 'input')

        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 20)

    @parameterized.expand([
        ('username', 'This field must not be empty'),
        ('last_name', 'write your last name'),
        ('first_name', 'write your first name'),
        ('password', 'Password must not be empty'),
        ('password2', 'This field must not be empty'),
    ])
    def test_empty_current_error_message(self, field, msg):
        # usuario abre a pagina de registro
        self.browser.get(self.live_server_url + '/authors/register')

        # ve um formulario com campos de cadastro
        form = self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form'
        )

        # preenche os campos com apenas um espaço em branco
        self.fill_form_dummy_data(form)

        # preenche o campo email com um email valido
        form.find_element(By.NAME, 'email').send_keys('email@gmail.com')

        # reescreve o campo atual com um espaço em branco
        current_field = form.find_element(By.NAME, field)
        current_field.send_keys(' ')

        # envia o formulario
        current_field.send_keys(Keys.ENTER)

        # vê os erros de preenchimento do formulario
        form = self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form'
        )
        self.sleep()
        # olha para o erro de preenchimento do campo atual
        self.assertIn(msg, form.text)
