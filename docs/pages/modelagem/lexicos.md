# <center>Lexicos

<div align="justify">

## 1. Introdução
A criação de léxicos é uma técnica que procura descrever os símbolos de uma linguagem. É comum que em meios sociais existam termos próprios relacionadas às ações e contextos do cotidiano, assim, os léxicos surgem com o objetivo de descrever os símbolos que denotam ações, atores ou estados que possuam representação única quando relacionada a um contexto específico.

## 2. Metodologia
A documentação dos léxicos foi realizada utilizando um modelo em tabelas informando a noção e o impacto do léxico, ou seja, as restrições impostas pelo/sobre o símbolo. A noção se refere ao significado do símbolo, sua denotação, e o impacto descreve os efeitos do uso do símbolo na aplicação, sua conotação.

## 3. Léxicos

### L1 - Profile

|            |  |
|:-------------|:-------|
| **Noção**    | > Indica a sessão de Perfil de Usuário;<br>> Simbolizado pela silhueta de uma pessoa.       |
| **Impacto**  | > O [professor](#l8-teacher) pode visualizar suas informações de cadastro na plataforma. |
| **Sinônimo** | > Perfil de usuário;<br>> Informações cadastrais;<br>> Informações pessoais.|

### L2 - Update Account

|            | |
|:-------------|:-------|
| **Noção**    | > Seção onde o [professor](#l8-teacher) pode alterar suas informações pessoais;<br> > Simbolizado por um lápis sobre papel.|
| **Impacto**  | > O [professor](#l8-teacher) pode alterar sua foto de perfil.<br> > O [professor](#l8-teacher) pode alterar nome de usuário;<br>> O [professor](#l8-teacher) pode alterar e-mail;<br>> O [professor](#l8-teacher) pode alterar A Instituição de ensino a qual pertence.<br>> O [professor](#l8-teacher) pode alterar a área do conhecimento a qual atua.|
| **Sinônimo** | > Atualizar conta;<br>> Atualizar perfil;<br>> Atualizar cadastro;<br>> Atualizar informações pessoais;|

### L3 - Update Password

|          |  |
|:-------------|:-------|
| **Noção**    | > Seção onde o [professor](#l8-teacher) pode alterar sua senha de acesso à plataforma;<br>> Simbolizado por um cadeado.|
| **Impacto**  | > O [professor](#l8-teacher) poderá modificar sua senha antiga pela senha desejada.|
| **Sinônimo** | > Atualizar senha;<br>> Modificar senha;<br>> Trocar senha.|

### L4 - Search Discipline

|            |  |
|:-------------|:-------|
| **Noção**    | > Seção onde o [professor](#l8-teacher) pode pesquisar qualquer disciplina cadastrada na plataforma;<br>> Simbolizado por uma lupa.|
| **Impacto**  | > A disciplina por ser pesquisada por nome;<br>> A disciplina pode ser pesquisada pelo [professor](#l8-teacher) responsável por ela;<br>> A disciplina pode ser pesquisada pelo título do curso ao qual faz parte.|
| **Sinônimo** | > Buscar disciplima;<br>> Procurar disciplina;<br>> Procurar matéria;<br>> Pesquisar disciplina;<br>> Pesquisar matéria.|

### L5 - Create Discipline

|            | |
|:-------------|:-------|
| **Noção**    | > Seção onde o [professor](#l8-teacher) pode criar uma disciplina;<br>> Simbolizada por um livro.|
| **Impacto**  | > A criação de uma disciplina permite que os alunos se inscrevam e tenham acesso aos conteúdos disponibilizados pelo [professor](#l8-teacher);<br>> O [professor](#l8-teacher) atribui um nome e o curso pelo qual a disciplina faz parte;<br>> O [professor](#l8-teacher) descreve sobre o que se trata a disciplina;<br>> O [professor](#l8-teacher) pode cadastrar monitores para uma disciplina.|
| **Sinônimo** | > Criar disciplina;<br>> Criar matéria;<br>> Cadastrar disciplina;<br>> Cadastrar matéria.|

### L6 - Create ClassRoom

|            |  |
|:-------------|:-------|
| **Noção**    | > Quando o [professor](#l8-teacher) cria uma [disciplina](#l5-create-discipline), atrelado a isso, é criada uma classroom.|
| **Impacto**  | > Alunos cadastrados na disciplina têm acesso à sala e aos conteúdos dela;<br>> Uma classroom permite a disponibilização de conteúdo para os alunos;<br>> Uma sala permite a criação de sessões TBL;<br>> O [professor](#l8-teacher) pode incluir arquivos à uma sala;<br>> O [professor](#l8-teacher) pode abrir fóruns de discussão em uma sala;<br>> O [professor](#l8-teacher) pode criar grupos em uma sala|
| **Sinônimo** | > Criar sala;<br>> Cadastrar sala;<br>> Criar ambiente de aula;<br>> Criar turma.|

### L7 - Send 

|            |  |
|:-------------|:-------|
| **Noção**    | > Botão responsável por efetivar a criação de uma [disciplina](#l5-create-discipline);<br>> Simbolizado por um sinal de "+" junto à palavra "_send_".|
| **Impacto**  | > Quando o [professor](#l8-teacher) necessitar criar uma [disciplina](#l5-create-discipline) é preciso efetivar esta criação clicando sobre o botão *Send*.|
| **Sinônimo** | > Enviar;<br>> Criar;<br>> Efetuar;<br>> Confirmar.|

### L8 - Teacher

| |  |
|:-------------|:-------|
| **Noção**    | > Rótulo atribuído ao usuário cadastrado com perfil de professor.|
| **Impacto**  | > O professor pode [criar uma disciplina](#l5-create-discipline);<br>> O professor pode [criar uma sala](#l6-create-classroom);<br>> O professor pode [visualizar uma disciplina](#l9-discipline-details);<br>> O professor pode [Resetar uma disciplina](#l10-reset-discipline);<br>> O professor pode [fechar uma disciplina](#l11-close-discipline);<br>> O professor pode visualizar a [lista de alunos](#l12-student-list);<br>> O professor pode visualizar as [notas finais](#l13-final-grades) dos alunos;<br>> O professor pode [criar grupos](#l14-groups);<br>> O professor pode criar sessões [TBL](#l15-tbl);<br>> O professor pode inserir [tags](#l16-tag) aos seus avisos;<br>> O professor pode criar [avaliações em grupo](#l20-grat);<br>> O professor pode criar [avaliações individuais](#l19-irat);<br>> O professor pode enviar [feedbacks](#l21-feedback) aos alunos.       |
| **Sinônimo** | > Professor;<br>> Mentor;<br>> Tutor;<br>> Docente;<br>> Educador;<br>> Orientador;<br>> Formador|

### L9 - Discipline Details

|        | |
|:-------------|:-------|
| **Noção**    | > Seção responsável por detalhar a [disciplina criada](#l5-create-discipline);<br>> Simbolizada por um livro.|
| **Impacto**  | > Quando o [professor](l8-teacher) cria uma [disciplina](#l5-create-discipline), é possível consultar as informações finais;<br>> É possível visualizar nome da disciplina;<br>> É possível visualizar área do conhecimento atrelada a disciplina;<br>> É possível visualizar nome do [professor](l8-teacher) responsável pela disciplina;<br>> É possível [fechar a disciplina](#l12-close-discipline);<br>> É possível [resetar](#l11-reset-discipline) uma disciplina.|
| **Sinônimo** | > Detalhes da disciplina;<br>> Detalhes da matéria;<br>> Infromações da disciplina;<br>> Informações da matéria;<br>> Dados da matéria;<br>> Dados da disciplina.|

### L10 - Reset Discipline

|             |    |
|:-------------|:-------|
| **Noção**    | > Resetar uma disciplina significa apagar todas as alterações realizadas sobre ela;<br>> Simbolizado por um botão vermelho com a inscrição "Reset discipline" |
| **Impacto**  | > Uma disciplina resetada é [fechada](#l12-close-discipline);<br>> Os [grupos](#l15-groups) são apagados;<br>> Os alunos são removidos das turmas;<br>> A disciplina deixa de aparecer no [perfil](#l1-profile) do [professor](#l8-teacher).|
| **Sinônimo** | > Deletar;<br>> Apagar;<br>> Resetar;<br>> Finalizar;<br>> Excluir;<br>> Extinguir;<br>> Eliminar;<br>> Remover.|

### L11 - Close Discipline

|             |    |
|:-------------|:-------|
| **Noção**    | > Uma disciplina só fica visível para terceiros se estiver habilitada como aberta;<br>> Simbolizado por um botão vermelho com a inscrição "Close discipline"|
| **Impacto**  | > A disciplina deixa de ficar visível para os alunos;<br>> Os alunos não poderão consultar materiais cadastrados naquela disciplina. |
| **Sinônimo** | > Fechar;<br>> Indisponibilixar;<br>> Pausar;<br>> Bloquear;<br>> Interromper;<br>> Paralizar.|

### L12 - Student List

|             |    |
|:-------------|:-------|
| **Noção**    | > Área onde são listados os alunos inscritos em disciplinas;<br>> Simbolizado pela silhueta de duas pessoas segurando um quadro.|
| **Impacto**  | > O [professor](#l8-teacher) pode visualizar a lista de alunos que se cadastraram em alguma de suas disciplinas;<br>> O professor pode consultar a matrícula e o email do aluno cadastrado;<br>> O professor pode consultar a quantidade de alunos inscritos em sua disciplina.|
| **Sinônimo** | > Listar alunos;<br>> Elencar alunos;<br>> Enumerar alunos.|

### L13 - Final Grades

|             |    |
|:-------------|:-------|
| **Noção**    | > Local destinado ao resumo das notas dos alunos no decorrer da disciplina;<br>> Simbolizado por um chapéu de formatura.|
| **Impacto**  | > Ao acessar a área de Final Grades, o [professor](#l8-teacher) pode visualizar todas as notas de cada aluno;<br>> O professor pode visualizar a média final de cada aluno.|
| **Sinônimo** | > Notas finais;<br>> Notas parciais;<br>> Hisórico de notas;<br>> Pontos.|

### L14 - Groups

|             |    |
|:-------------|:-------|
| **Noção**    | > As disciplinas podem ter grupos de alunos associados a elas, a critério do [professor](#l8-teacher);<br>> Simbolizado pelas silhuetas de 3 pessoas.|
| **Impacto**  | > O professor pode adicionar alunos aos grupos;<br>> O professor pode editar as informações dos grupos;<br>> O professor pode apagar grupos.|
| **Sinônimo** | > Equipe;<br>> Grupo de trabalho.|

### L15 - TBL

|             |    |
|:-------------|:-------|
| **Noção**    | > Team Based Learning é um módulo ou unidade educacional baseada em equipe.|
| **Impacto**  | > Toda a plataforma é baseada neste modelo.|
| **Sinônimo** | > Aprendizado Baseado em Times.|

### L16 - Tag

|             |    |
|:-------------|:-------|
| **Noção**    | > Palavras-chave sobre um assunto em um fórum de avisos.|
| **Impacto**  | > As tags facilitam a busca por um assunto dentro de um fórum.|
| **Sinônimo** | > Label;<br>> Palavra-chave;<br>> String de busca.|

### L17 - Preparação

|             |    |
|:-------------|:-------|
| **Noção**    | > Etapa responsável pelo estudo individual dos alunos pré classe para se prepararem para o [RAT](#l18-rat)|
| **Impacto**  | > O aluno não preparado terá baixo desempenho na [avaliação individual](#l19-irat);<br>> O aluno não preparado terá baixo desempenho em [grupo](#l14-groups)      |
| **Sinônimo** |        |

### L18 - RAT

|             |    |
|:-------------|:-------|
| **Noção**    | > Readiness assurance test (Avaliação de garantia de preparo) é a atividade que deve ser realizada de [maneira individual](#l19-irat) e [em grupo](#l20-grat).|
| **Impacto**  | > Impacta nas sessões TBL pois através dela existirá a porcentagem da nota da sessões.|
| **Sinônimo** | > Teste;<br>> Simulado;<br>> Avaliação formativa.|

### L19 - iRAT

|             |    |
|:-------------|:-------|
| **Noção**    | > Individual Readiness Assurance Test ou iRAT é a avaliação individual que os alunos devem realizar. |
| **Impacto**  | > Um aluno com bom desempenho no iRAT tem suas notas finas altas;<br>> Um aluno com baixo desempenho no iRAT tem notas finais baixas.|
| **Sinônimo** | > Avaliação individual|

### L20 - gRAT

|             |    |
|:-------------|:-------|
| **Noção**    | > Group Readiness Assurance Test ou gRAT é a avaliação em grupo que os alunos devem realizar.|
| **Impacto**  | > Essa avaliação impacta na nota de grupo e individual.|
| **Sinônimo** | > Trabalho em grupo;<br>> Avaliação em grupo.|

### L21 - Feedback

|             |    |
|:-------------|:-------|
| **Noção**    | > Retornos que o [professor](#l8-teacher) dará ao aluno sobre os tópicos abordados no [TBL](#l15-tbl)|
| **Impacto**  | > Essa avaliação impacta na [nota de grupo](#l20-grat) e [individual](#l19-irat).|
| **Sinônimo** | > Trabalho em grupo;<br>> Avaliação em grupo.|

</div>

## Bibliografia 

SAYÃO, M.; LEITE, C.. **Rastreabilidade de Requisitos**. Universidade Católica do Rio de Janeiro, Rio de Janeiro, 2005.

#### Histórico de Versão
| Data       | Versão | Descrição                  | Autor(es)          |
|:----------:|:------:|:--------------------------:|:------------------:|
| 10.11.2020 | 0.1    | Criação do documento       | Rafaella Junqueira |