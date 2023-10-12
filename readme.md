# Django Recipes

Um aplicativo de registro de receitas desenvolvido com Django.

## Sobre

Este aplicativo permite que os usuários criem, editem e compartilhem receitas. Os usuários podem pesquisar receitas por título, ingrediente ou categoria.

## Recursos

* Criação de receitas
* Edição de receitas
* Compartilhamento de receitas
* Pesquisa de receitas
* Instalação
* Para instalar o aplicativo, siga estas etapas:

## Clone o repositório do GitHub

```
git clone https://github.com/MarcusViniciusBarcelos/curso-django.git
```

2. Crie um ambiente virtual e ative-o:

```
python3 -m venv venv
source venv/bin/activate
```

3. Instale as dependências:

```
pip install -r requirements.txt
```

4. Crie um banco de dados e configure as configurações:

```
python manage.py migrate
```

5. Crie um superusuário:

```
python manage.py createsuperuser
```

6. Inicie o servidor:

```
python manage.py runserver
```

## Uso

Para usar o aplicativo, abra um navegador e navegue para <http://localhost:8000>.

## Contribuições

Contribuições são bem-vindas. Para contribuir, crie um fork do repositório e envie um pull request.

## Licença

Este projeto é licenciado sob a licença MIT.
