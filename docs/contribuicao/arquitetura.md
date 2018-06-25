# Arquitetura
***
## 1 Objetivos
***

O objetivo desse tópico é apresentar e detalhar a arquitetura que será utilizada na plataforma TBL. Dessa maneira, visa-se atingir um entendimento mútuo entre os desenvolvedores do projeto, de forma que seja entendida a estrutura utilizada para desenvolver o software, além das consequências que a escolha de tal arquitetura implica.

Este tópico visa estabelecer de forma clara as especificidades sobre as decisões arquiteturais para que as consequências diminuam os riscos e que qualquer pessoa consiga evoluir e manter o software. O desenvolvedor que ler esse documento obterá uma visão geral de como esse software está estruturado.

***
## 2 Representação Arquitetural
***

![arquitetura](https://user-images.githubusercontent.com/14116020/38155355-b1b6269c-344d-11e8-82a2-dcb89ed534f4.png)

1 - O **web client (navegador)** manda uma requisição para o **web server (Nginx)** com o protocolo HTTP.

2 - Os arquivos estáticos armazenados no sistema de arquivos, como CSS, JavaScript, Imagens e documentos PDF, podem ser processados diretamente pelo **web server (Nginx)**.

3 - A parte dinâmica é delegada ao servidor de aplicativos WSGI (Web Server Gateway Interface) do django, no caso o gunicorn que é um servidor WSGI para Unix feito em python puro, ele irá converter solicitações HTTP recebidas do servidor em chamadas python em colaboração com o framework django que irá ter um arquivo chamado urls.py que diz ao nginx qual código deverá ser executado de acordo com o path e código HTTP recebido, através de proxy reverso será feito o redirecionamento inicial do Nginx com o servidor da aplicação, ou seja, o proxy reverso irá funcionar como uma ponte de ligação entre o nginx e o django através do gunicorn.

4 - Dentro do django a requisição recebida pelo **web server** é mapeado para uma view especifica através das urls, a view pede dados a modelo, a model pega os dados do banco de dados postgresql e retorna a view, a view seleciona o template e fornece os dados, com isso o template é preenchido e devolvido a view, a view devolve o template como resposta ao web server.

5 - O web server (nginx) retorna a resposta para o web client (navegador)

A arquitetura utilizada no projeto será o arquitetura de microserviços.

O projeto será implementado utilizando o framework [Django](https://www.djangoproject.com/) na versão 1.11. O django utiliza-se do MVT (Model-View-Template) como uma adaptação do MVC (Model-View-Controller), o que muda é que a view do MVC virou template do MVT e a controller do MVC virou view do MVT, nas views utilizaremos as [Classe Based Views](http://ccbv.co.uk/). Esse framework fará comunicação com o banco de dados Postgresql e o servidor nginx.

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

***
## 3. Diagrama de classe
***

Um diagrama de classe UML descreve o objeto e informações de estruturas usadas pelo seu aplicativo, internamente e comunicação com seus usuários. Ele descreve as informações sem referência a qualquer implementação específica.[[1](https://msdn.microsoft.com/pt-br/library/dd409437.aspx)]

**Observação**: Os diagramas abaixo vão ser criados ao longo do projeto.

![diagrama_de_classe_atualizado](https://user-images.githubusercontent.com/16181794/41073053-d4cf29de-69d7-11e8-8a4c-95315bb8ed93.jpg)

***
## 4. Framework i*
***

O framework de modelagem i* (i-estrela), originalmente proposto por Yu, trata da modelagem de contextos organizacionais tomando como base os relacionamentos de dependência entre os atores participantes.
 
O principal objetivo no i* é representar, através de modelos, os atores participantes e as dependências entre os mesmos, para que suas metas próprias sejam alcançadas, recursos sejam fornecidos, tarefas sejam realizadas e metas flexíveis sejam “razoavelmente satisfeitas”.
 
Podemos ler suas dependências da seguinte forma: Ator1 depende do ator2 para atingir uma meta, ou fornecer um recurso ou realizar uma tarefa, e etc...
 
De acordo com a legenda os atores são divididos em 3 que são os agentes, posições e papéis, no caso um agente ocupa uma posição e realiza um papel, tendo como relação de dependência as metas, tarefas, recursos e _softgoals_

_Softgoals_ são os requisitos não funcionais definido no [Framework NFR](nfr)
 
### 4.1 Modelo SD (modelo de dependências estratégicas)
 
O modelo SD exibe os relacionamentos de dependência estratégica entre os atores da organização, utilizando para isso uma rede de nós, representando os atores (agentes, posições ou papéis) e arestas, representando as dependências entre os mesmos.

![i__sd](https://user-images.githubusercontent.com/14116020/27992013-bb6c5c06-645f-11e7-9c90-8883bce39840.png)

### 4.2 Modelo SR (modelo de dependências estratégicas)
 
Enquanto o modelo SD trata apenas dos relacionamentos externos entre os atores, o modelo SR é utilizado para descrever os relacionamentos internos. Ele possibilita a avaliação das possíveis alternativas de definição do processo, investigado mais detalhadamente as razões existentes, ou intencionalidades, por trás das dependências entre os atores.

Assim como o SD, o modelo SR também é composto por ligações de dependência:

* **Means-ends**: As ligações de meio-fim indicam um relacionamento entre um nó fim e um meio para atingi-lo.

* **Decomposition**: Já as ligações de decomposição de tarefas ligam um nó de tarefa a seus nós componentes, que segundo [Yu 1995] podem ser outras tarefas, objetivos, recursos ou objetivos-soft, nesse diagrama foi utilizado dois tipos de decomposição de tarefas:

   - **AND e AND**: todas vão acontecer.

   - **AND e OR**: uma irá acontecer a outra pode ou não acontecer

   - **OR e OR**: uma das duas irá acontecer.

![i__sr](https://user-images.githubusercontent.com/14116020/38155590-fc4b12ca-344e-11e8-82fc-45183b9712f5.png)

***
## 5. Framework NFR
***

O NFR Framework é uma abordagem orientada a processos, onde os requisitos não-funcionais são explicitamente representados como metas a serem obtidas e como serão obtidas

![nfr](https://user-images.githubusercontent.com/14116020/38151244-db3c13ba-3438-11e8-9574-530599729541.png)

***
## 6. MER
***

O Modelo Entidade Relacionamento (também chamado Modelo ER, ou simplesmente MER), como o nome sugere, é um modelo conceitual utilizado na Engenharia de Software para descrever os objetos (entidades) envolvidos em um domínio de negócios, com suas características (atributos) e como elas se relacionam entre si (relacionamentos).

Em geral, este modelo representa de forma abstrata a estrutura que possuirá o banco de dados da aplicação. Obviamente, o banco de dados poderá conter várias outras entidades, tais como chaves e tabelas intermediárias, que podem só fazer sentido no contexto de bases de dados relacionais.

A partir das informações obtidas, esse modelo conceitual será utilizado para orientar o desenvolvimento propriamente dito, fornecendo informações sobre os aspectos relacionados ao domínio do projeto em questão. [[devmedia](http://www.devmedia.com.br/modelo-entidade-relacionamento-mer-e-diagrama-entidade-relacionamento-der/14332)]

### Entidades e Atributos

#### <a name="tags">Tags</a>

|Atributo|Tipo|Característica|Descrição|
|--------|----|--------------|---------|
|title|string|obrigatório|Título da tag|
|slug|string|obrigatório|Usado para inserir URLs nomeadas|

#### <a name="news">News</a>

|Atributo|Tipo|Característica|Descrição|
|--------|----|--------------|---------|
|title|string|obrigatório|Título da notícia|
|image|Image|opcional|Imagem da notícia|
|created_at|date|automático|Data de criação da noticia|
|link|string|opcional|Link da notícia|
|content|string|obrigatório|corpo da notícia|
|tags|List<[Tag](#tags)>|opcional|tags da notícia|
|slug|string|obrigatório|Usado para inserir URLs nomeadas|

#### <a name="user">User</a>:

|Atributo|Tipo|Característica|Descrição|
|--------|----|--------------|---------|
|username|string|obrigatório, único|Nome de usuário para identificação do mesmo, pode ser usado para logar|
|email|string|obrigatório, único|Email que pode ser usado como username do usuário|
|name|string|obrigatório|Nome completo do usuário|
|institution|string|opcional|Universidade ou Escola que o usuário está inserido|
|course|string|opcional|Curso da universidade ou período escolar|
|photo|image|opcional|Foto do usuário|
|is_teacher|boolean|obrigatório|Verifica se o usuário é professor ou aluno|
|last_login|date|automático|Ultimo momento que o usuário logou|
|is_active|boolean|obrigatório|Verifica se o usuário está ativo no sistema|
|is_staff|boolean|obrigatório|Verifica se o usuário é super administrador|
|created_at|date|automático|Data de criação da conta|
|updated_at|date|automático|Data de modificação da informações da conta|

#### <a name="discipline">Discipline</a>:

|Atributo|Tipo|Característica|Descrição|
|--------|----|--------------|---------|
|title|string|obrigatório|Título da disciplina|
|description|string|opcional|Descrição da disciplina|
|course|string|obrigatório|Curso na qual pertence a disciplina|
|slug|string|obrigatório|Usado para inserir URLs nomeadas|
|classroom|string|obrigatório|Turmas da disciplina|
|password|string|30 caracteres, optativa|Senha para entrar na disciplina|
|students_limit|inteiro positivo|valor máximo 60 e minimo 5, padrão 0 e obrigatório|Limite de estudantes na turma|
|monitors_limit|inteiro positivo|valor máximo 5 e minimo 0, padrão 0 e obrigatório|Limite de monitores na turma|
|is_closed|booleano|padrão falso|Verifica se a disciplina ta fechada ou não|
|was_group_prodived|booleano|padrão falso|Disponibiliza os grupos para os alunos verem|
|teacher|[User](#user)|obrigatório|Professor da disciplina|
|students|List<[User](#user)>|obrigatório|Lista de estudantes da disciplina|
|monitors|List<[User](#user)>|obrigatório|Lista de monitores da disciplina|
|created_at|date|automático|Data de criação da disciplina|
|updated_at|date|automático|Data de modificação da disciplina|

#### <a name="group">Group</a>:

|Atributo|Tipo|Característica|Descrição|
|--------|----|--------------|---------|
|title|string|obrigatório|Título do grupo|
|discipline|[Discipline](#discipline)|obrigatório|Disciplina na qual o grupo pertence|
|students|List<[User](#user)>|obrigatório|Lista de estudantes que faz parte do grupo|
|students_limit|inteiro positivo|padrão 0 e obrigatório|Limite de estudantes no grupo|
|created_at|date|automático|Data de criação do grupo|
|updated_at|date|automático|Data de modificação do grupo|

#### <a name="final_grade">FinalGrade</a>:

|Atributo|Tipo|Característica|Descrição|
|--------|----|--------------|---------|
|discipline|[Discipline](#discipline)|obrigatório|Disciplina que a nota pertence|
|student|[User](#user)|obrigatório|Aluno dono da nota.|
|created_at|date|automático|Data de criação da nota|
|updated_at|date|automático|Data de modificação da nota|

#### <a name="file">File</a>:

|Atributo|Tipo|Característica|Descrição|
|--------|----|--------------|---------|
|discipline|[Discipline](#discipline)|obrigatorio|Disciplina na qual o TBL pertence.|
|title|string|obrigatório|Título do arquivo|
|description|string|obrigatório|Descrição do arquivo|
|extension|string|obrigatório|Extensão do arquivo, PDF, PPT, ...|
|archive|File|obrigatório|Arquivo|
|created_at|date|automático|Data de criação do arquivo|
|updated_at|date|automático|Data de modificação do arquivo|

#### <a name="discipline_file">DisciplineFile: [File](#file)</a>:

#### <a name="tblsession">TBLSession</a>

|Atributo|Tipo|Característica|Descrição|
|--------|----|--------------|---------|
|discipline|[Discipline](#discipline)|obrigatorio|Disciplina na qual o TBL pertence.|
|title|string|obrigatório|Título da sessão de TBL|
|description|string|obrigatório|Descrição da sessão de TBL|
|is_closed|booleano|padrão falso|Verifica se a sessão ta fechada ou não|
|irat_datetime|datetime|obrigatório|Data e hora que será disponibilizado a avaliação iRAT|
|irat_weight|inteiro positivo|opcional, padrão 3|Peso da avaliação iRAT|
|irat_duration|inteiro positivo|opcional, padrão 30|Duração da avaliação iRAT em minutos|
|grat_datetime|datetime|obrigatório|Data e hora que será disponibilizado a avaliação gRAT|
|grat_weight|inteiro positivo|opcional, padrão 2|Peso da avaliação gRAT|
|grat_duration|inteiro positivo|opcional, padrão 30|Duração da avaliação gRAT em minutos|
|practical_available|boolean|padrão false|Verifica se a avaliação prática está visivel pelos alunos|
|practical_description|string|obrigatório|Descrição da avaliação prática|
|practical_weight|inteiro positivo|opcional, padrão 4|Peso da avaliação prática|
|peer_review_available|boolean|padrão false|Verifica se a avaliação em pares está visivel pelos alunos|
|peer_review_weight|inteiro positivo|opcional, padrão 1|Peso da avaliação em pares|
|created_at|date|automático|Data de criação da sessão de TBL|
|updated_at|date|automático|Data de modificação da sessão de TBL|

#### <a name="grade">Grade</a>:

|Atributo|Tipo|Característica|Descrição|
|--------|----|--------------|---------|
|session|[Session](#session)|obrigatório|Sessão TBL que a nota pertence|
|student|[User](#user)|obrigatório|Aluno dono da nota.|
|group|[Group](#group)|obrigatorio|Grupo a qual o estudante pertence.|
|iRAT|float|automático, padrão 0|Nota da avaliação individual do aluno|
|gRAT|float|automático, padrão 0|Nota da avaliação em grupo do aluno|
|practical|float|automático, padrão 0|Nota da avaliação prática|
|peer_review|float|automático|Nota da avaliação em pares|
|created_at|date|automático|Data de criação da nota|
|updated_at|date|automático|Data de modificação da nota|

#### <a name="session_file">SessionFile: [File](#file)</a>:

|Atributo|Tipo|Característica|Descrição|
|--------|----|--------------|---------|
|session|[Session](#session)|obrigatório|Sessão TBL que o arquivo pertence|

#### <a name="question">Question</a>:

|Atributo|Tipo|Característica|Descrição|
|--------|----|--------------|---------|
|session|[Session](#session)|obrigatório|Sessão TBL que a questão pertence|
|title|string|obrigatório|Título da questão|
|level|string|obrigatório|Nível de dificuldade da questão|
|topic|string|obrigatório|Tópico da questão|
|is_exercise|boolean|padrão true|Verifica se a questão é um exercício ou uma avaliação|
|created_at|date|automático|Data de criação da questão|
|updated_at|date|automático|Data de modificação da questão|

#### <a name="alternative">Alternative</a>:

|Atributo|Tipo|Característica|Descrição|
|--------|----|--------------|---------|
|question|[Question](#question)|obrigatório|Questão na qual a alternativa pertence|
|title|string|obrigatório|Título da alternativa|
|is_correct|boolean|padrão false|Verifica se a alternativa está correta|
|created_at|date|automático|Data de criação da alternativa|
|updated_at|date|automático|Data de modificação da alternativa|

#### <a name="submission">Submission</a>:

|Atributo|Tipo|Característica|Descrição|
|--------|----|--------------|---------|
|correct_alternative|string|obrigatório|Título da alternativa correta|
|score|inteiro positivo|obrigatório, padrao 0|Pontuação da alternativa|
|created_at|date|automático|Data de criação da submissão|

#### <a name="exercise_submission">ExerciseSubmission: [Submission](#submission)</a>:

|Atributo|Tipo|Característica|Descrição|
|--------|----|--------------|---------|
|session|[Session](#session)|obrigatório|Sessão TBL que a submissão foi realizada|
|question|[Question](#question)|obrigatório|Questão da lista de exercicio respondida|
|user|[User](#user)|obrigatório|Usuário que submeteu a questão|

#### <a name="irat_submission">IRATSubmission: [Submission](#submission)</a>:

|Atributo|Tipo|Característica|Descrição|
|--------|----|--------------|---------|
|session|[Session](#session)|obrigatório|Sessão TBL que a submissão foi realizada|
|question|[Question](#question)|obrigatório|Questão da avaliação iRAT respondida|
|user|[User](#user)|obrigatório|Estudante que submeteu a questão|

#### <a name="grat_submission">GRATSubmission: [Submission](#submission)</a>:

|Atributo|Tipo|Característica|Descrição|
|--------|----|--------------|---------|
|session|[Session](#session)|obrigatório|Sessão TBL que a submissão foi realizada|
|question|[Question](#question)|obrigatório|Questão da avaliação gRAT respondida|
|user|[User](#user)|obrigatório|Estudante do grupo que submeteu a questão|
|group|[Group](#group)|obrigatório|Grupo que submeteu a questão|

#### <a name="ranking">Ranking</a>:

Atributo | Tipo	| Característica | Descrição
---------|------|----------------|----------
discipline_id | Discipline | obrigatório | Disciplina na qual o Ranking de grupos pertence.

#### <a name="group_info">GroupInfo</a>:

Atributo | Tipo	| Característica | Descrição
---------|------|----------------|----------
results | float | automático, padrão 0 | Nota de desempenho do grupo com a média de todas as suas avaliações iRAT, gRAT, prática e em pares.
group_id | Group | obrigatório | Grupo na qual estas informações pertencem.
ranking_id | Ranking | obrigatório | Ranking de grupos no qual este GroupInfo está vinculado.  

#### <a name="hall_of_fame">HallOfFame</a>:

Atributo | Tipo	| Característica | Descrição
---------|------|----------------|----------
year | inteiro positivo | obrigatório | Ano no qual este objeto do HallOfFame pertence.
semester | inteiro positivo | opcional, padrão 0 | Semestre no qual este objeto do HallOfFame pertence.
discipline_id | Discipline | obrigatório | Disciplina no qual este objeto do HallOfFame pertence.
group_info_id | GroupInfo | obrigatório | GroupInfo vinculado a este objeto do HallOfFame.

### Relacionamentos entre classes

NEWS tem TAGS:

- Uma noticia pode ter várias tags, e uma tag pode estar em várias noticias
- **Cardinalidade**: NxM

DISCIPLINE tem USER (Professor):

- Uma disciplina tem um professor, e um professor pode ter várias disciplinas.
- **Cardinalidade**: Nx1

DISCIPLINE tem USER (Estudante):

- Uma disciplina pode ter vários estudantes, e um estudante pode estar em várias disciplinas.
- **Cardinalidade**: NxM

DISCIPLINE tem USER (Monitor):

- Uma disciplina pode ter vários monitores, e um monitor pode estar em várias disciplinas.
- **Cardinalidade**: NxM

GROUP tem USER (Estudante):

- Um grupo pode ter vários estudantes, e um estudante pode estar em vários grupos.
- **Cardinalidade**: NxM

GROUP pertence DISCIPLINE:

- Um grupo pertencer a uma disciplina, porém uma disciplina poder ter vários grupos.
- **Cardinalidade**: Nx1

DISCIPLINEFILE pertence DISCIPLINE:

- Um arquivo pertencer a uma disciplina, porém uma disciplina poder ter vários arquivos.
- **Cardinalidade**: Nx1

FINALGRADE pertence DISCIPLINE:

- Uma nota pertencer a uma disciplina, porém uma disciplina poder ter vários notas.
- **Cardinalidade**: Nx1

FINALGRADE pertence USER (Estudante):

- Uma nota pertencer a um estudante, porém um estudante poder ter várias notas.
- **Cardinalidade**: Nx1

TBLSESSION pertence DISCIPLINE:

- Uma sessão de TBL pertencer a uma disciplina, porém uma disciplina poder ter várias sessões de TBL.
- **Cardinalidade**: Nx1

SESSIONFILE pertence TBLSESSION:

- Um arquivo pertencer a uma sessão de TBL, porém uma sessão de TBL poder ter vários arquivos.
- **Cardinalidade**: Nx1

GRADE pertence TBLSESSION:

- Um nota pertencer a uma sessão de TBL, porém uma sessão de TBL poder ter várias notas.
- **Cardinalidade**: Nx1

GRADE pertence USER (Estudante):

- Um nota pertencer a um estudante, porém um estudante poder ter várias notas.
- **Cardinalidade**: Nx1

GRADE pertence GROUP:

- Um nota pertencer a uma grupo, porém uma grupo poder ter várias notas.
- **Cardinalidade**: Nx1

QUESTION pertence TBLSESSION:

- Um questão pertencer a sessão de TBL, porém uma sessão de TBL poder ter várias questões.
- **Cardinalidade**: Nx1

ALTERNATIVE pertence QUESTION:

- Uma alternativa pertencer a uma questão, porém uma questão tem 4 alternativas.
- **Cardinalidade**: 4x1

SUBMISSION pertence TBLSESSION:

- Uma submissão (exercise, iRAT e gRAT) pertencer a sessão de TBL, porém uma sessão de TBL poder ter várias submissões.
- **Cardinalidade**: Nx1

SUBMISSION pertence QUESTION:

- Uma submissão (exercise, iRAT e gRAT) pertence a uma questão, porém uma questão poder ter várias submissões.
- **Cardinalidade**: Nx1

SUBMISSION pertence USER:

- Uma submissão (exercise, iRAT e gRAT) pertence a um usuário, porém um usuário poder ter várias submissões.
- **Cardinalidade**: Nx1

SUBMISSION pertence GROUP:

- Uma submissão (gRAT) pertence a um grupo, porém um grupo poder ter várias submissões.
- **Cardinalidade**: Nx1

RANKING tem DISCIPLINE:

- Um ranking de grupos deve ter uma disciplina, e uma disciplina deve ter um rankings de grupos.
- Cardinalidade: 1x1

GROUPINFO tem GROUP:

- Uma informações de um grupo deve ter um grupo, e um grupo deve ter uma informações de um grupo.
- **Cardinalidade:** 1x1

GROUPINFO tem RANKING:

- Uma informações de um grupo deve ter um ranking de grupo, e um ranking de grupos pode ter várias informações de grupos.
- **Cardinalidade:** Nx1

HALLOFFAME tem DISCIPLINE:

- Um hall da fama deve ter uma disciplina, e uma disciplina pode ter vários halls da fama.
- **Cardinalidade:** Nx1

GROUPINFO pertence HALLOFFAME:

- Uma informações de um grupo pode pertencer a um hall da fama, porém um hall da fama pode ter várias infromações de um grupo.
- **Cardinalidade:** Nx1

***
## Referências
***

Istar Wiki. Disponível em:  <http://istar.rwth-aachen.de/tiki-view_articles.php> Acesso em 17 de abril de 2017.
