# MER - Modelo Entidade Relacionamento
***

O Modelo Entidade Relacionamento (também chamado Modelo ER, ou simplesmente MER), como o nome sugere, é um modelo conceitual utilizado na Engenharia de Software para descrever os objetos (entidades) envolvidos em um domínio de negócios, com suas características (atributos) e como elas se relacionam entre si (relacionamentos).

Em geral, este modelo representa de forma abstrata a estrutura que possuirá o banco de dados da aplicação. Obviamente, o banco de dados poderá conter várias outras entidades, tais como chaves e tabelas intermediárias, que podem só fazer sentido no contexto de bases de dados relacionais.

A partir das informações obtidas, esse modelo conceitual será utilizado para orientar o desenvolvimento propriamente dito, fornecendo informações sobre os aspectos relacionados ao domínio do projeto em questão. [[devmedia](http://www.devmedia.com.br/modelo-entidade-relacionamento-mer-e-diagrama-entidade-relacionamento-der/14332)]

***
## Entidades e Atributos
***

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

***
## Relacionamentos entre classes
***

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
