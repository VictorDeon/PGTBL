# Instalações
***
### Linux
***

Pega o repositorio do github: ```git clone https://github.com/VictorArnaud/PGTBL.git```

Instalar dependencias para rodar o python3 e pip3

```sh
sudo apt-get update
  
sudo apt-get install -y python3-dev sqlite python3-pip libpq-dev
sudo apt-get install -y gettext
```

Criar o ambiente virtual de desenvolvimento (virtualenvwrapper)

```sh
sudo pip3 install --upgrade pip
sudo pip3 install virtualenvwrapper
```

No arquivo .bashrc do link insira:

```sh
WORKON_HOME=~/.virtualenvs
VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
source /usr/local/bin/virtualenvwrapper.sh
```

- Para criar um ambiente virtual: ```mkvirtualenv <venv_name>```

- Para entrar no ambiente virtual: ```workon <venv_name>```

- Para sair do ambiente virtual: ```deactivate```

Instalar dependencias do projeto dentro do ambiente virtual

```sh
pip install -r pgtbl/requeriments.txt
```

Rodar comandos para popular o banco de dados

```sh
make migrations
make migrate
make superuser
```

Rode o servidor

```sh
make run
```

***
### Docker
***

Instale o docker: https://docs.docker.com/install/linux/docker-ce/ubuntu/

Execute o comando no diretorio do projeto:

```sh
docker-compose up -d
```

Obs: Se der erro tente com o sudo na frente do comando.
