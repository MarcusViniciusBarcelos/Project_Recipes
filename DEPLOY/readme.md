# Deploy

Aqui estão os dados de referência para deploy da aplicação

### Chaves SSH

Para criar chaves ssh no seu computador, utilize o comando ssh-keygen. Se você
já tem chaves SSH no computador e por algum motivo queira usar outra, use o
comando:

```
ssh-keygen -t rsa -b 4096 -f CAMINHO+NOME_DA_CHAVE
```

Lembre-se que a pasta .ssh deve existir dentro da pasta do seu usuário para que
seja possível criar a chave SSH. Muito comum ocorrer erros no Windows por falta
dessa pasta.

Para conectar-se ao servidor usando uma chave SSH com caminho personalizado,
utilize:

```
ssh IP_OU_HOST -i CAMINHO+NOME_DA_CHAVE
```

### Ao entrar no servidor

A primeira coisa será atualizar tudo:

```
sudo apt update -y
sudo apt upgrade -y
sudo apt autoremove -y
sudo apt install build-essential -y
sudo apt install python3.9 python3.9-venv python3.9-dev -y
sudo apt install nginx -y
sudo apt install certbot python3-certbot-nginx -y
sudo apt install libpq-dev -y
sudo apt install git
```

## Instalando o PostgreSQL

```
sudo apt install postgresql postgresql-contrib -y
```

### Configurações

```
sudo -u postgres psql
# Criando um super usuário
CREATE ROLE usuario WITH LOGIN SUPERUSER CREATEDB CREATEROLE PASSWORD 'senha';
# Criando a base de dados
CREATE DATABASE basededados WITH OWNER usuario;
# Dando permissões
GRANT ALL PRIVILEGES ON DATABASE basededados TO usuario;
# Saindo
\q
sudo systemctl restart postgresql
```

## Configurando o git

```
git config --global user.name 'Seu nome'
git config --global user.email 'seu_email@gmail.com'
git config --global init.defaultBranch main
```

## Criando um repositório no servidor

Um repositório bare é um repositório transitório (como se fosse um github).

```
mkdir -p ~/app_bare
cd ~/app_bare
git init --bare
cd ~
```

Criando o repositório da aplicação

```
mkdir -p ~/app_repo
cd ~/app_repo
git init
git remote add origin ~/app_bare
git add . && git commit -m 'Initial'
cd ~
```

No seu computador local, adicione o bare como remoto:

```
git remote add app_bare cursodjangoserver:~/app_bare
git push app_bare <branch>
```

No servidor, em app_repo, faça pull:

```
cd ~/app_repo
git pull origin <branch>
```

## Criando o ambiente virtual

```
cd  ~/app_repo
git pull origin <branch>
python3.9 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
pip install psycopg2
pip install gunicorn
```
