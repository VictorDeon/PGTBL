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

O projeto será implementado utilizando o framework [Django](https://www.djangoproject.com/) na versão 2.0. O django utiliza-se do MVT (Model-View-Template) como uma adaptação do MVC (Model-View-Controller), o que muda é que a view do MVC virou template do MVT e a controller do MVC virou view do MVT, nas views utilizaremos as [Classe Based Views](http://ccbv.co.uk/). Esse framework fará comunicação com o banco de dados Postgresql e o servidor nginx.

#### 2.1 Pacotes Significativos do Ponto de Vista da Arquitetura

![package](https://user-images.githubusercontent.com/14116020/50112829-62700780-0227-11e9-9e7c-c44b7e9c6d9a.png)

Os pacotes dos apps:

* **locale**: Pasta que irá ter toda a tradução do software para pt-BR.
* **migrations**: pasta com todas as migrações das modelos para o banco, são os SQLs.
* **static**: É onde fica os arquivos estáticos da aplicação (CSS, JS e IMG)
* **templates**: É onde fica os templates da aplicação (HTML)
* **tests**: contém os testes automatizados feitos no sistema.
* **__init__**: É o arquivo que define que sua pasta é um pacote python.
* **admin**: contém a instância da modelo que fará parte do sistema de administração do django, lá pode-se fazer CRUD das models.
* **app**: arquivo que contém informações da aplicação do django.
* **forms**: pasta que contém os campos que será inserido no formularios
* **models**: pasta de arquivos que faz interface com o banco de dados, é responsável por leitura, validação e escrita de dados no banco de dados.
* **permissions**: Arquivo de implementação de permissões do aplicativo.
* **urls**: São as rotas para ser acessada pelo navegador
* **views**: pasta que contém a camada lógica do sistema e a comunicação com o navegador por meio de rotas (Classe Based Views).
* **fixtures**: pasta que contém arquivos json para pré-popular o banco de dados para testes manuais

Os pacotes do projeto settings:

* **config**: É uma pasca que contém as configurações do software separada em arquivos.
* **settings**: São as configurações gerais do software importadas da pasta config.
* **urls**: Arquivo que terá o mapeamento de rotas de todo o projeto com todas as aplicações.
* **wsgi**: Arquivo usado para deploy do projeto.

Os pacotes do projeto pgtbl:

* **manage**: Arquivo de configuração geral do django.

Os pacotes gerais do projeto:

* **Vagrantfile**: Arquivo que gerencia a máquina virtual de desenvolvimento, criado para desenvolvedores que queiram desenvolver em sistemas operacionais diferentes do Linux, como Windows ou Mac, precisa ter o [Vagrant](https://www.vagrantup.com/docs/installation/) instalado.
* **Makefile**: Arquivo de atalhos para comandos muito usados pelos desenvolvedores.
* **requirements**: Pasta de arquivos para instalar dependências da aplicação através do seguinte comando ```pip3 install -r requirements-dev.txt``` ou ```pip3 install -r requirements-prod.txt``` dependendo do ambiente na qual você quer instalar as dependências.
* **docker-compose**: Arquivos que gerencia todos os containers da aplicação (deploy, homolog, production, test e
  desenvolvimento).
* **.travis**: Arquivo que gerencia a entrega continua da aplicação através da ferramenta Travis CI no github.
* **.codacy**: Arquivo de configuração da ferramenta de análise estática de código Codacy.
* **.gitignore**: Arquivo que faz o git ignorar alguns arquivos do projeto.
* **README**: Arquivo com um conteúdo markdown inicial do projeto.
* **LICENSE**: Licença do software.
* **mkdocs**: Arquivo que contém a configuração da documentação do software.
* **prototype**: Pasta com o protótipo do software.
* **docs**: Pasta com toda a documentação do software.
* **makefiles**: Pasta que contém de forma organizada comandos do Makefile.
* **images**: Pasta que armazena as imagens de deploy da aplicação tbl.
* **scripts**: Pasta com alguns scripts de integração e deploy continuo

***
## 3. Diagrama de classe
***

Um diagrama de classe UML descreve o objeto e informações de estruturas usadas pelo seu aplicativo, internamente e comunicação com seus usuários. Ele descreve as informações sem referência a qualquer implementação específica.[[1](https://msdn.microsoft.com/pt-br/library/dd409437.aspx)]

**Observação**: Os diagramas abaixo vão ser criados ao longo do projeto.

![diagramadeclasse](https://user-images.githubusercontent.com/14116020/50118869-33ae5d00-0238-11e9-9623-65a1c7f4f4d6.png)

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

![i__sr](https://user-images.githubusercontent.com/14116020/40564986-3174de68-6041-11e8-9b78-2b853ddc4ded.png)

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
|content|string|obrigatório|corpo da notícia|
|link|string|opcional|Link da notícia|
|image|Image|opcional|Imagem da notícia|
|tags|List<[Tag](#tags)>|opcional|tags da notícia|
|created_at|date|automático|Data de criação da noticia|
|slug|string|obrigatório|Usado para inserir URLs nomeadas|

#### <a name="user">User</a>:

|Atributo|Tipo|Característica|Descrição|
|--------|----|--------------|---------|
|username|string|obrigatório, único|Nome de usuário para identificação do mesmo, pode ser usado para logar|
|name|string|obrigatório|Nome completo do usuário|
|email|string|obrigatório, único|Email que pode ser usado como username do usuário|
|institution|string|opcional|Universidade ou Escola que o usuário está inserido|
|course|string|opcional|Curso da universidade ou período escolar|
|photo|image|opcional|Foto do usuário|
|last_login|date|automático|Ultimo momento que o usuário logou|
|created_at|date|automático|Data de criação da conta|
|updated_at|date|automático|Data de modificação da informações da conta|
|is_active|boolean|obrigatório|Verifica se o usuário está ativo no sistema|
|is_staff|boolean|obrigatório|Verifica se o usuário é super administrador|
|is_teacher|boolean|obrigatório|Verifica se o usuário é [professor](#l8-teacher) ou aluno|

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
|teacher|[User](#user)|obrigatório|[professor](#l8-teacher) da disciplina|
|students|List<[User](#user)>|obrigatório|Lista de estudantes da disciplina|
|monitors|List<[User](#user)>|obrigatório|Lista de monitores da disciplina|
|created_at|date|automático|Data de criação da disciplina|
|updated_at|date|automático|Data de modificação da disciplina|
|objects|DisciplineManager|automático|Gerenciador de disciplinas do Django|

#### <a name="notification">Notification</a>:

|Atributo|Tipo|Característica|Descrição|
|--------|----|--------------|---------|
|discipline|[Discipline](#discipline)|obrigatório|Disciplina na qual a notificação foi enviada|
|title|string|obrigatório|Título da notificação|
|description|string|opcional|Descrição da notificação|
|sender|[User](#user)|obrigatório|Quem enviou a notificação|
|receiver|[User](#user)|obrigatório|Quem recebeu a notificação|
|created_at|date|automático|Data de criação da notificação|

#### <a name="group">Group</a>:

|Atributo|Tipo|Característica|Descrição|
|--------|----|--------------|---------|
|title|string|obrigatório|Título do grupo|
|discipline|[Discipline](#discipline)|obrigatório|Disciplina na qual o grupo pertence|
|students_limit|inteiro positivo|padrão 0 e obrigatório|Limite de estudantes no grupo|
|students|List<[User](#user)>|obrigatório|Lista de estudantes que faz parte do grupo|
|created_at|date|automático|Data de criação do grupo|
|updated_at|date|automático|Data de modificação do grupo|

#### <a name="final_grade">FinalGrade</a>:

|Atributo|Tipo|Característica|Descrição|
|--------|----|--------------|---------|
|discipline|[Discipline](#discipline)|obrigatório|Disciplina que a nota pertence|
|student|[User](#user)|obrigatório|Aluno dono da nota.|
|final_grade|float|obrigatório|Nota final do aluno|
|status|string|obrigatório|Status final do aluno (aprovado ou reprovado)|
|created_at|date|automático|Data de criação da nota|
|updated_at|date|automático|Data de modificação da nota|

#### <a name="halloffame">HallOfFameGroup</a>:

|Atributo|Tipo|Característica|Descrição|
|--------|----|--------------|---------|
|discipline|[Discipline](#discipline)|obrigatório|Disciplina na qual o hall of fame pertence|
|title|string|obrigatório|Título do grupo|
|students|List<[User](#user)>|obrigatório|Lista de estudantes que faz parte do grupo que ganhou o hall of fame|
|gamification_score|integer|obrigatório|Pontuação total do grupo na gamificação|
|first_position_once|boolean|obrigatório, default False|O grupo ficou pelo menos uma vez em primeiro lugar em uma sessão de TBL|
|first_position_always|boolean|obrigatório, default False|O grupo sempre ficou em primeiro lugar nas sessões de TBL|
|created_at|date|automático|Data de criação do grupo|

#### <a name="file">File</a>:

|Atributo|Tipo|Característica|Descrição|
|--------|----|--------------|---------|
|title|string|obrigatório|Título do arquivo|
|description|string|obrigatório|Descrição do arquivo|
|extension|string|obrigatório|Extensão do arquivo, PDF, PPT, ...|
|archive|File|obrigatório|Arquivo|
|created_at|date|automático|Data de criação do arquivo|
|updated_at|date|automático|Data de modificação do arquivo|

#### <a name="topic">Topic</a>:

|Atributo|Tipo|Característica|Descrição|
|--------|----|--------------|---------|
|title|string|obrigatório|Título do tópico do fórum|
|content|string|obrigatório|Conteúdo do tópico do fórum|
|tags|List<Tag>|obrigatório|Tag que qualifica e categoriza o tópico|
|views|integer|obrigatório, default 0|Quantidade de pessoas que visualizou o tópico|
|author|[User](#user)|obrigatório|Usuário que criou o tópico, pode ser [professor](#l8-teacher), aluno ou monitor|
|discipline|[Discipline](#discipline)|obrigatório|Disciplina na qual tópico do fórum pertence|
|qtd_answers|integer|obrigatório, default 0|Quantidade de respostas tem o tópico|
|created_at|date|automático|Data de criação do tópico|
|updated_at|date|automático|Data de modificação do tópico|

#### <a name="answer">Answer</a>:

|Atributo|Tipo|Característica|Descrição|
|--------|----|--------------|---------|
|author|[User](#user)|obrigatório|Usuário que respondeu o tópico, pode ser [professor](#l8-teacher), aluno ou monitor|
|topic|[Topic](#topic)|obrigatório|Tópico na qual a resposta pertence|
|content|string|obrigatório|Conteúdo da resposta do tópico|
|is_correct|boolean|obrigatório, default False|Especifica qual é a resposta correta.|
|created_at|date|automático|Data de criação do tópico|
|updated_at|date|automático|Data de modificação do tópico|

#### <a name="discipline_file">DisciplineFile: [File](#file)</a>:

|Atributo|Tipo|Característica|Descrição|
|--------|----|--------------|---------|
|discipline|[Discipline](#discipline)|obrigatorio|Disciplina na qual o TBL pertence.|

#### <a name="tblsession">TBLSession</a>

|Atributo|Tipo|Característica|Descrição|
|--------|----|--------------|---------|
|discipline|[Discipline](#discipline)|obrigatorio|Disciplina na qual o TBL pertence.|
|title|string|obrigatório|Título da sessão de TBL|
|description|string|obrigatório|Descrição da sessão de TBL|
|is_closed|booleano|padrão falso|Verifica se a sessão ta fechada ou não|
|is_finished|booleano|padrão falso|Verifica se a sessão ta finalizada, ou seja, suas notas serão geradas e fechadas permanentemente|
|irat_datetime|datetime|obrigatório|Data e hora que será disponibilizado a avaliação iRAT|
|irat_weight|inteiro positivo|opcional, padrão 3|Peso da avaliação iRAT|
|irat_duration|inteiro positivo|opcional, padrão 30|Duração da avaliação iRAT em minutos|
|grat_datetime|datetime|obrigatório|Data e hora que será disponibilizado a avaliação gRAT|
|grat_weight|inteiro positivo|opcional, padrão 2|Peso da avaliação gRAT|
|grat_duration|inteiro positivo|opcional, padrão 30|Duração da avaliação gRAT em minutos|
|practical_available|boolean|padrão false|Verifica se a avaliação prática está visivel pelos alunos|
|practical_weight|inteiro positivo|opcional, padrão 4|Peso da avaliação prática|
|practical_description|string|obrigatório|Descrição da avaliação prática|
|peer_review_available|boolean|padrão false|Verifica se a avaliação em pares está visivel pelos alunos|
|peer_review_weight|inteiro positivo|opcional, padrão 1|Peso da avaliação em pares|
|created_at|date|automático|Data de criação da sessão de TBL|
|updated_at|date|automático|Data de modificação da sessão de TBL|

#### <a name="grade">Grade</a>:

|Atributo|Tipo|Característica|Descrição|
|--------|----|--------------|---------|
|session|[TBLSession](#session)|obrigatório|Sessão TBL que a nota pertence|
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
|session|[TBLSession](#session)|obrigatório|Sessão TBL que o arquivo pertence|

#### <a name="question">Question</a>:

|Atributo|Tipo|Característica|Descrição|
|--------|----|--------------|---------|
|title|string|obrigatório|Título da questão|
|session|[TBLSession](#session)|obrigatório|Sessão TBL que a questão pertence|
|level|string|obrigatório|Nível de dificuldade da questão|
|topic|string|obrigatório|Tópico da questão|
|is_exercise|boolean|padrão true|Verifica se a questão é um exercício ou uma avaliação|
|created_at|date|automático|Data de criação da questão|
|updated_at|date|automático|Data de modificação da questão|

#### <a name="alternative">Alternative</a>:

|Atributo|Tipo|Característica|Descrição|
|--------|----|--------------|---------|
|title|string|obrigatório|Título da alternativa|
|question|[Question](#question)|obrigatório|Questão na qual a alternativa pertence|
|is_correct|boolean|padrão false|Verifica se a alternativa está correta|
|created_at|date|automático|Data de criação da alternativa|
|updated_at|date|automático|Data de modificação da alternativa|

#### <a name="exercise_submission">ExerciseSubmission</a>:

|Atributo|Tipo|Característica|Descrição|
|--------|----|--------------|---------|
|correct_alternative|string|obrigatório|Título da alternativa correta|
|score|inteiro positivo|obrigatório, padrao 0|Pontuação da alternativa|
|session|[TBLSession](#session)|obrigatório|Sessão TBL que a submissão foi realizada|
|question|[Question](#question)|obrigatório|Questão da lista de exercicio respondida|
|user|[User](#user)|obrigatório|Usuário que submeteu a questão|
|created_at|date|automático|Data de criação da submissão|

#### <a name="irat_submission">IRATSubmission</a>:

|Atributo|Tipo|Característica|Descrição|
|--------|----|--------------|---------|
|correct_alternative|string|obrigatório|Título da alternativa correta|
|score|inteiro positivo|obrigatório, padrao 0|Pontuação da alternativa|
|session|[TBLSession](#session)|obrigatório|Sessão TBL que a submissão foi realizada|
|question|[Question](#question)|obrigatório|Questão da avaliação iRAT respondida|
|user|[User](#user)|obrigatório|Estudante que submeteu a questão|
|created_at|date|automático|Data de criação da submissão|

#### <a name="grat_submission">GRATSubmission</a>:

|Atributo|Tipo|Característica|Descrição|
|--------|----|--------------|---------|
|correct_alternative|string|obrigatório|Título da alternativa correta|
|score|inteiro positivo|obrigatório, padrao 0|Pontuação da alternativa|
|session|[TBLSession](#session)|obrigatório|Sessão TBL que a submissão foi realizada|
|question|[Question](#question)|obrigatório|Questão da avaliação gRAT respondida|
|user|[User](#user)|obrigatório|Estudante do grupo que submeteu a questão|
|created_at|date|automático|Data de criação da submissão|
|group|[Group](#group)|obrigatório|Grupo que submeteu a questão|

#### <a name="peer_review_submission">PeerReviewSubmission</a>:

|Atributo|Tipo|Característica|Descrição|
|--------|----|--------------|---------|
|session|[TBLSession](#session)|obrigatório|Sessão TBL que a submissão foi realizada|
|score|inteiro positivo|obrigatório, padrao 0|Pontuação da avaliação|
|comment|string|opcional|Comentário anônimo da avaliação de peer review|
|user|[User](#user)|obrigatório|Estudante do grupo que submeteu a peer review|
|student|[User](#user)|obrigatório|Estudante do grupo que recebeu a peer review|
|group|[Group](#group)|obrigatório|Grupo do aluno que submeteu a peer review|
|created_at|date|automático|Data de criação da submissão|

#### <a name="gamification_submission">GamificationPointSubmission</a>:

|Atributo|Tipo|Característica|Descrição|
|--------|----|--------------|---------|
|session|[TBLSession](#session)|obrigatório|Sessão TBL que a submissão foi realizada|
|student|[User](#user)|obrigatório|Estudante que fez a pontuação|
|group|[Group](#group)|obrigatório|Grupo do aluno que fez a pontuação|
|total_score|inteiro positivo|obrigatório, padrao 0|Pontuação total do aluno|
|first_position|booleano|obrigatório, padrao False|Verifica se o grupo ficou em primeiro lugar na sessão de TBL|
|created_at|date|automático|Data de criação da submissão|

#### <a name="appeal">Appeal</a>:

|Atributo|Tipo|Característica|Descrição|
|--------|----|--------------|---------|
|title|string|obrigatório|Título da apelação|
|description|string|obrigatório|Corpo da apelação|
|is_accept|boolean|obrigatório, default False|Verifica se a apelação foi aceita ou não pelo [professor](#l8-teacher)|
|qtd_comments|integer|obrigatório, default 0|Quantidade de comentários da apelação|
|question|[Question](#question)|obrigatório|Questão na qual a apelação foi submetida|
|student|[User](#user)|obrigatório|Estudante que fez solicitou a apelação|
|group|[Group](#group)|obrigatório|Grupo do estudante que solicitou a apelação|
|session|[TBLSession](#session)|obrigatório|Sessão TBL que a apelação foi submetida|
|created_at|date|automático|Data de criação da submissão|
|updated_at|date|automático|Data de atualização da submissão|

#### <a name="comment">Comment</a>:

|Atributo|Tipo|Característica|Descrição|
|--------|----|--------------|---------|
|author|[User](#user)|obrigatório|Usuário que comentou na apelação do colega|
|appeal|[Appeal](#appeal)|obrigatório|Apelação na qual o comentário foi feito|
|content|string|obrigatório|Corpo do comentário|
|created_at|date|automático|Data de criação da submissão|
|updated_at|date|automático|Data de atualização da submissão|

### Relacionamentos entre classes

NEWS tem TAGS:

- Uma noticia pode ter várias tags, e uma tag pode estar em várias noticias
- **Cardinalidade**: NxM

DISCIPLINE tem USER ([professor](#l8-teacher)):

- Uma disciplina tem um [professor](#l8-teacher), e um [professor](#l8-teacher) pode ter várias disciplinas.
- **Cardinalidade**: Nx1

DISCIPLINE tem USER (Estudante):

- Uma disciplina pode ter vários estudantes, e um estudante pode estar em várias disciplinas.
- **Cardinalidade**: NxM

DISCIPLINE tem USER (Monitor):

- Uma disciplina pode ter vários monitores, e um monitor pode estar em várias disciplinas.
- **Cardinalidade**: NxM

TOPIC pertence USER:

- Um tópico do fórum é criado por um usuário, e um usuário pode criar vários tópicos.
- **Cardinalidade**: Nx1

TOPIC pertence DISCIPLINE:

- Um tópico do fórum pertence a uma disciplina, e uma disciplina pode ter vários tópicos.
- **Cardinalidade**: Nx1

ANSWER pertence USER:

- Uma resposta ao tópico do fórum é criado por um usuário, e um usuário pode inserir várias respostas.
- **Cardinalidade**: Nx1

ANSWER pertence TOPIC:

- Uma resposta pertence a um tópico do fórum, e um tópico do fórum pode ter várias respostas, mas apenas 1 correta.
- **Cardinalidade**: Nx1

NOTIFICATION pertence DISCIPLINE:

- Uma notificação é enviada por meio de uma disciplina, e uma disciplina pode ter várias notificações
- **Cardinalidade**: Nx1

NOTIFICATION é enviado USER:

- Uma notificação é enviada por um usuário, e um usuário pode enviar várias notificações.
- **Cardinalidade**: Nx1

NOTIFICATION é recebido USER:

- Uma notificação é recebida por um usuário, e um usuário pode receber várias notificações.
- **Cardinalidade**: Nx1

GROUP tem USER (Estudante):

- Um grupo pode ter vários estudantes, e um estudante pode estar em vários grupos.
- **Cardinalidade**: NxM

GROUP pertence DISCIPLINE:

- Um grupo pertencer a uma disciplina, porém uma disciplina poder ter vários grupos.
- **Cardinalidade**: Nx1

HALL OF FAME GROUP pertence DISCIPLINE:

- Um grupo no hall of fame pertencer a uma disciplina, porém uma disciplina poder ter vários grupos no hall of fame.
- **Cardinalidade**: Nx1

HALL OF FAME GROUP tem USER:

- Um grupo no hall of fame tem vários estudantes, porém um estudante pertence a um único grupo do hall of fame da disciplina.
- **Cardinalidade**: 1xN

DISCIPLINE FILE pertence DISCIPLINE:

- Um arquivo pertencer a uma disciplina, porém uma disciplina poder ter vários arquivos.
- **Cardinalidade**: Nx1

FINAL GRADE pertence DISCIPLINE:

- Uma nota pertencer a uma disciplina, porém uma disciplina poder ter vários notas.
- **Cardinalidade**: Nx1

FINAL GRADE pertence USER (Estudante):

- Uma nota pertencer a um estudante, porém um estudante poder ter várias notas.
- **Cardinalidade**: Nx1

TBL SESSION pertence DISCIPLINE:

- Uma sessão de TBL pertencer a uma disciplina, porém uma disciplina poder ter várias sessões de TBL.
- **Cardinalidade**: Nx1

SESSION FILE pertence TBL SESSION:

- Um arquivo pertencer a uma sessão de TBL, porém uma sessão de TBL poder ter vários arquivos.
- **Cardinalidade**: Nx1

GRADE pertence TBL SESSION:

- Um nota pertencer a uma sessão de TBL, porém uma sessão de TBL poder ter várias notas.
- **Cardinalidade**: Nx1

GRADE pertence USER (Estudante):

- Um nota pertencer a um estudante, porém um estudante poder ter várias notas.
- **Cardinalidade**: Nx1

GRADE pertence GROUP:

- Um nota pertencer a uma grupo, porém uma grupo poder ter várias notas.
- **Cardinalidade**: Nx1

QUESTION pertence TBL SESSION:

- Um questão pertencer a sessão de TBL, porém uma sessão de TBL poder ter várias questões.
- **Cardinalidade**: Nx1

ALTERNATIVE pertence QUESTION:

- Uma alternativa pertencer a uma questão, porém uma questão tem 4 alternativas.
- **Cardinalidade**: 4x1

SUBMISSION pertence TBL SESSION:

- Uma submissão (exercise, iRAT e gRAT) pertencer a sessão de TBL, porém uma sessão de TBL poder ter várias submissões.
- **Cardinalidade**: Nx1

SUBMISSION pertence QUESTION:

- Uma submissão (exercise, iRAT e gRAT) pertence a uma questão, porém uma questão poder ter várias submissões.
- **Cardinalidade**: Nx1

SUBMISSION pertence USER:

- Uma submissão (exercise, iRAT e gRAT) pertence a um usuário, porém um usuário poder ter várias submissões.
- **Cardinalidade**: Nx1

GRAT_SUBMISSION pertence GROUP:

- Uma submissão (gRAT) pertence a um grupo, porém um grupo poder ter várias submissões gRAT.
- **Cardinalidade**: Nx1

PEER REVIEW SUBMISSION pertence TBL SESSION:

- Uma submissão (peer review) pertence a uma sessão de TBL, e uma sessão de TBL pode ter várias submissões Peer Review
- **Cardinalidade**: Nx1

PEER REVIEW SUBMISSION pertence USER:

- Uma submissão (peer review) é enviada por um estudante, e um estudante pode enviar várias submissões Peer Review para colegas diferentes.
- **Cardinalidade**: Nx1

PEER REVIEW SUBMISSION pertence USER:

- Uma submissão (peer review) é recebida por um estudante, e um estudante pode receber várias submissões Peer Review de colegas diferentes.
- **Cardinalidade**: Nx1

PEER REVIEW SUBMISSION pertence GROUP:

- Uma submissão (peer review) pertence a um estudante do grupo, e um grupo pode receber várias submissões Peer Review de colegas diferentes.
- **Cardinalidade**: Nx1

GAMIFICATION POINT SUBMISSION pertence TBL SESSION:

- Uma submissão (gamificação) pertence a uma sessão de TBL, e uma sessão de TBL pode ter várias submissões de gamificação
- **Cardinalidade**: Nx1

GAMIFICATION POINT SUBMISSION pertence USER:

- Uma submissão (gamificação) é conquistada por um estudante, e um estudante pode conquistar várias submissões de gamificação.
- **Cardinalidade**: Nx1

GAMIFICATION POINT SUBMISSION pertence GROUP:

- Uma submissão (gamificação) pertence a um estudante do grupo, e um grupo pode conquistar várias submissões de gamificação.
- **Cardinalidade**: Nx1

APPEAL pertence QUESTION:

- Uma apelação pertence a uma questão, e uma questão pode ter várias apelações
- **Cardinalidade**: Nx1

APPEAL pertence TBL SESSION:

- Uma apelação pertence a uma sessão de TBL, e uma sessão de TBL pode ter várias apelações
- **Cardinalidade**: Nx1

APPEAL pertence USER:

- Uma apelação é enviada por um estudante, e um estudante pode enviar várias apelações
- **Cardinalidade**: Nx1

APPEAL pertence GROUP:

- Uma apelação é enviada por um estudante de um grupo, e um grupo pode ter várias apelações de estudantes diferentes.
- **Cardinalidade**: Nx1

COMMENT pertence USER:

- Um comentário é enviada por um estudante para uma apelação, e um estudante pode enviar várias comentários para essa apelação
- **Cardinalidade**: Nx1

COMMENT pertence APPEAL:

- Um comentário pertence a uma apelação, e uma apelação pode ter vários comentários
- **Cardinalidade**: Nx1


***
## Referências
***

Istar Wiki. Disponível em:  <http://istar.rwth-aachen.de/tiki-view_articles.php> Acesso em 17 de abril de 2017.
