## Instalações
***
#### Linux
***

Pega o repositorio do github: ```git clone <repository_url>```

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
pip install -r requeriments.txt
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
#### Vagrant
***

Neste tópico serão abordadas as etapas para configuração do ambiente de desenvolvimento do projeto. Este será desenvolvido em Python/Django. Utilizamos para o desenvolvimento uma Máquina Virtual configurada com o Vagrant e com o Virtual Box atuando como provider.

Os passos para configuração do ambiente estão definidos abaixo.

1 - O primeiro passo é o clone do [repositório](https://github.com/VictorArnaud/TBL)

2 - O próximo passo é a instalação do [Vagrant](https://www.vagrantup.com/downloads.html) e do [virtual box](https://www.virtualbox.org/wiki/Downloads) a forma de instalação depende do seu sistema operacional, caso utilize o windows baixe o [GIT BASH](git-scm.com) utilizando a configuração Unix Tool.

3 - Execute o ```vagrant up``` no repositório que tem o **Vagrantfile** para criar a máquina, isso irá instalar tudo que estiver dentro do provision "shell" especificado no Vagrantfile, ele instalará automaticamente o projeto para desenvolvimento.

4 - Execute o ```Vagrant ssh``` para entrar na máquina, o repositório do projeto estará em **/home/vagrant** dentro da máquina é só da o comando ```cd /home/vagrant```

5 - Ao sair da máquina lembre-se de fecha-la com um ```vagrant halt```. Se quiser entrar novamente só executar o ```vagrant up```.

6 - Dentro do vagrant você precisa executar o comando ```mkvirtualenv nome_do_ambiente --python=python3```, isso irá criar o ambiente de desenvolvimento para instalar as dependências do software. Podemos sair do ambiente com o comando ```deactivate``` e entrar novamente nele com o comando ```workon nome_do_ambiente```.

7 - Dentro do ambiente você precisa instalar todos os pacotes do software, incluindo o django, esses pacotes se encontram no arquivo **requirements.txt** e você pode instala-los com o comando ```pip3 install -r requeriments.txt``` se der algum problema de permissão insira o sudo na frente.

Com isso você já pode começar a desenvolver o sistema, tem vários comandos/atalhos dentro do arquivo **Makefile** que pode facilitar sua vida no desenvolvimento.

***
#### Docker
***

