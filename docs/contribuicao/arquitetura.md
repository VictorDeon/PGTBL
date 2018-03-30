## 1 Objetivos

O objetivo desse tópico é apresentar e detalhar a arquitetura que será utilizada na plataforma TBL. Dessa maneira, visa-se atingir um entendimento mútuo entre os desenvolvedores do projeto, de forma que seja entendida a estrutura utilizada para desenvolver o software, além das consequências que a escolha de tal arquitetura implica.

Este tópico visa estabelecer de forma clara as especificidades sobre as decisões arquiteturais para que as consequências diminuam os riscos e que qualquer pessoa consiga evoluir e manter o software. O desenvolvedor que ler esse documento obterá uma visão geral de como esse software está estruturado.

## 2 Representação Arquitetural

A arquitetura utilizada no projeto será o estilo arquitetural **MVC**.

O projeto será implementado utilizando o framework [Django](https://www.djangoproject.com/) na versão 1.11. O django utiliza-se do MVT (Model-View-Template) como uma adaptação do MVC (Model-View-Controller), o que muda é que a view do MVC virou template do MVT e a controller do MVC virou view do MVT, nas views utilizaremos as [Classe Based Views](http://ccbv.co.uk/).

#### 2.1 Pacotes Significativos do Ponto de Vista da Arquitetura

![package](https://user-images.githubusercontent.com/14116020/36355763-e065e10e-14c6-11e8-9fef-fdd8b4d33ed1.png)

Os pacotes dos apps:

* **locale**: Pasta que irá ter toda a tradução do software para pt-BR.
* **migrations**: pasta com todas as migrações das modelos para o banco, são os SQLs.
* **static**: É onde fica os arquivos estáticos da aplicação (CSS, JS e IMG)
* **templates**: É onde fica os templates da aplicação (HTML)
* **tests**: contém os testes unitários feitos no sistema.
* **__init__**: É o arquivo que define que sua pasta é um pacote python.
* **admin**: contém a instância da modelo que fará parte do sistema de administração do django, lá pode-se fazer CRUD das models.
* **app**: arquivo que contém informações da aplicação do django.
* **forms**: contém os campos que será inserido no formularios
* **model**: faz interface com o banco de dados, é responsável por leitura, validação e escrita de dados no banco de dados.
* **permissions**: Arquivo de implementação de permissões do aplicativo.
* **urls**: São as rotas para ser acessada pelo navegador
* **view**: contém a camada lógica do sistema e a comunicação com a API por meio de rotas (Classe Based Views).

Os pacotes do projeto settings:

* **config**: É uma pasca que contém as configurações do software separada em arquivos.
* **settings**: São as configurações gerais do software importadas da pasta config.
* **urls**: Arquivo que terá o mapeamento de rotas de todo o projeto com todas as aplicações.
* **wsgi**: Arquivo usado para deploy do projeto.

Os pacotes gerais do projeto tbl:

* **Vagrantfile**: Arquivo que gerencia a máquina virtual de desenvolvimento, criado para desenvolvedores que queiram desenvolver em sistemas operacionais diferentes do Linux, como Windows ou Mac, precisa ter o [Vagrant](https://www.vagrantup.com/docs/installation/) instalado.
* **Dockerfile**: Arquivo que gerencia o container de deploy da aplicação tbl.
* **docker-compose**: Arquivo que gerencia todos os containers de deploy da aplicação.
* **.travis**: Arquivo que gerencia a entrega continua da aplicação através da ferramenta Travis CI no github.
* **Makefile**: Arquivo de atalhos para comandos muito usados pelos desenvolvedores.
* **requirements**: Arquivos para instalar dependências da aplicação através do seguinte comando ```pip3 install -r requirements.txt```
* **manage**: Arquivo de configuração geral do django.

### 2.2 Modelo

![arquitetura](https://user-images.githubusercontent.com/14116020/36355764-e085d73e-14c6-11e8-8802-ac83e8799db7.png)
