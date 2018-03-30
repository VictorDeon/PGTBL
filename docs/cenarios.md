# Cenários
***

Trata-se de uma estratégia reconhecida para compreender as interações entre ambientes e sistemas, assim como elicitar a parte comportamental do software, sua dinâmica e/ou seu fluxo.

### Cenário 01: Registro
 
|||
|-----|-----|
|**Título**|Registro|
|**Contexto**|Registro do professor e do aluno no sistema|
|**Objetivo**|Descrever como funciona o registro do professor e do aluno no software|
|**Atores**|Professor e Aluno|
|**Recursos**|Software|
|**Episódios**|O professor ou o aluno entra na url do software, cadastra sua conta, com seus dados pessoais como nome, email (identificador único), senha e se ele é aluno ou professor, com isso o sistema irá devolver a conta para que o professor ou o aluno passa logar no sistema, podendo atualizar seus dados pessoais ou mudar a senha.|
 
### Cenário 02: Disciplina
 
|||
|-----|-----|
|**Título**|Disciplina|
|**Contexto**|Criação da disciplina|
|**Objetivo**|Descrever como funciona a criação da disciplina pelo professor no software|
|**Atores**|Professor|
|**Recursos**|Software|
|**Episódios**|O professor autenticado no sistema irá criar a disciplina especificando a turma que irá ministrar aula e disponibilizar para que os alunos se cadastre para usufruir do TBL, cada turma terá um número máximo de alunos e pode ser fechada mesmo se esse número de alunos não seja completado.|
 
### Cenário 03: Alunos
 
|||
|-----|-----|
|**Título**|Aluno entrando na turma|
|**Contexto**|Alunos entrando em disciplina/turma|
|**Objetivo**|Descrever como funciona desde a pesquisa até a inserção do aluno na turma de um disciplina|
|**Atores**|Aluno|
|**Recursos**|Software|
|**Episódios**|O aluno irá pesquisar as disciplinas que foram criadas pelos professores, a pesquisa pode ser filtrada por professor, disciplina ou turma, ao clicar na disciplina irá mostrar as informações da disciplina e a sua respectiva turma, com isso ele poderá ter acesso a turma através de uma senha que será disponibilizado pelo professor que a criou|
 
### Cenário 04: Grupos
 
|||
|-----|-----|
|**Título**|Grupos|
|**Contexto**|Montagem dos grupos de alunos de cada turma|
|**Objetivo**|Descrever como funciona a montagem dos grupos de alunos no software|
|**Atores**|Professor e Aluno|
|**Recursos**|Software|
|**Episódios**|O professor irá fechar a turma caso não tenha batido o limite de alunos, ou se bater fechará automaticamente, com isso o professor irá montar os grupos inserindo alunos de forma fácil e organizada, podendo editar os grupos antes da lista ser disponibilizada para os alunos olharem quem são os membros do seu grupo.|

### Cenário 05: Sessões de TBL
 
|||
|-----|-----|
|**Título**|Criar sessões do TBL|
|**Contexto**|Professor criará as sessões do TBL|
|**Objetivo**|Descrever como funciona a criação das sessões do TBL.|
|**Atores**|Professor|
|**Recursos**|Software|
|**Episódios**|O professor irá criar as sessões de TBL na qual poderá ter uma quantidade n de sessões no semestre, uma sessão terá as 3 atividades básicas do TBL que é Preparação, RAT e Avaliação prática, e opcionalmente terá a avaliação em pares que o professor pode disponibilizar em uma sessão ou não, ao criar a sessão o professor poderá edita-la como quiser até disponibilizar ao alunos entrarem e começarem a utilizar os recursos da sessão, ao final de cada sessão o software cria uma tabela com as notas dos alunos e atualiza o rank de grupos|


### Cenário 06: Preparação
 
|||
|-----|-----|
|**Título**|Preparação - material|
|**Contexto**|Preparação dos alunos para as avaliações da sessão|
|**Objetivo**|Descrever como funciona a etapa de preparação no software através dos materiais disponibilizados|
|**Atores**|Professor e Aluno|
|**Recursos**|Software|
|**Episódios**|O professor irá disponibilizar o material de estudo para que os alunos passam baixar e se preparar para a avaliação iRAT e gRAT, esse material pode ser um artigo, livro, etc... além de ter um local para a leitura dinâmica de alguma material preparado pelo professor.|

### Cenário 07: Lista de exercicios
 
|||
|-----|-----|
|**Título**|Preparação - Lista de exercicios|
|**Contexto**|Lista de exercícios para o aluno estudar|
|**Objetivo**|Descrever como funciona a etapa de criação e disponibilização da lista de exercícios na etapa de preparação|
|**Atores**|Professor e aluno|
|**Recursos**|Software|
|**Episódios**|Quando o professor disponibilizar o material para os alunos estudarem ele fará uma lista com uma quantidade grande de exercícios, essa lista pode ser armazenada e utilizada em outros semestres, as questões criadas na lista será de múltipla escolha e quando a lista for respondida dará o feedback ao aluno da resposta correta, no final terá o resultado final com sua nota, essa nota é só para o aluno ter uma ideia se ta ou não preparado para as avaliações seguintes, essa lista de questões criadas servirá de base para criar as avaliações, a lista pode ser editada quando quiser pelo professor.|
 
### Cenário 08: Avaliação RAT
 
|||
|-----|-----|
|**Título**|Criar avaliação RAT|
|**Contexto**|Professor irá criar a avaliação iRAT e gRAT|
|**Objetivo**|Descrever como funciona a criação das avaliação individuais iRAT e em grupo gRAT|
|**Atores**|Professor|
|**Recursos**|Software|
|**Episódios**|Assim que a lista de exercício for criada, o professor irá separar algumas questões para ser inseridas nas avaliações, as questões das avaliações não estarão presentes na lista de exercícios, dentro da avaliação o professor poderá editar as questões, a data da avaliação e seu peso na nota do aluno e o tempo para responde-la, com isso assim que chegar na data especificada o aluno terá acesso a avaliação.|

### Cenário 09: Avaliação iRAT e gRAT
 
|||
|-----|-----|
|**Título**|Avaliação iRAT e gRAT|
|**Contexto**|Avaliação individual iRAT e em grupo gRAT|
|**Objetivo**|Descrever como funciona a etapa de avaliação no software|
|**Atores**|Professor e Aluno|
|**Recursos**|Software|
|**Episódios**|No dia da avaliação o sistema irá disponibilizar a avaliação individual _iRAT_ para os alunos responderem, a avaliação é de múltipla escolha na qual o aluno poderá distribuir pontos entre as 4 opções tendo 4 pontos para isso e terá um tempo limite para responder, esgotando esse tempo a avaliação será fechada, e em seguida na data estipulada pelo professor irá ser disponibilizado a avaliação em grupo _gRAT_ na qual os alunos dos grupos irão se reunir e responder a avaliação, também terá um tempo e somente um aluno do grupo irá submeter à avaliação, ela será de múltipla escolha e terá o layout de raspadinha como feedback, os alunos vão ter 4 opções para distribuir entre as 4 alternativas, a primeira opção vale 4 pontos, segunda 2 pontos, terceira 1 ponto e quarta nenhum ponto, com isso se a alternativa correta for a que o aluno marcou como opção 01 o grupo ganha 4 pontos na questão e será mostrado o layout de raspadinha para o aluno verificar sua resposta, não é obrigatorio, no final de ambas as avaliações terá uma tabela com o resultado de cada questão e a nota final da avaliação.|
 
### Cenário 10: Relatorio
 
|||
|-----|-----|
|**Título**|Relatorio|
|**Contexto**|Professor irá receber um relatório no seu dashboard|
|**Objetivo**|Descrever como o software gera o relatorio e disponibiliza para o professor|
|**Atores**|Professor|
|**Recursos**|Software|
|**Episódios**|Assim que o iRAT e o gRAT forem submetidos o professor irá receber um relatório em forma de gráfico com a quantidade de acertos e erros em cada questão da prova, tendo um feedback para verificar o que os alunos estão tendo dificuldades e tirar suas dúvidas em aula para que eles possam realizar a avaliação prática e aprender o conteúdo.|
 
### Cenário 11: Recurso
 
|||
|-----|-----|
|**Título**|Recurso|
|**Contexto**|Alunos entraram com recurso em algum questão|
|**Objetivo**|Descreve como é o processo para entrar em recurso|
|**Atores**|Professor e Aluno|
|**Recursos**|Software|
|**Episódios**|Assim que terminar as avaliações iRAT e gRAT, os alunos já receberam um feedback das respostas da avaliação, caso algum aluno discorde da resposta ele deve enviar ao professor um recurso com o número da questão, e a justificativa do porque a questão deve ser anulada, o professor irá receber esse recurso e avaliar, se for viável ele poderá mudar a nota dos alunos se não for nada acontece.|
 
### Cenário 12: Avaliação prática
 
|||
|-----|-----|
|**Título**|Avaliação prática|
|**Contexto**|Professor irá criar e disponibilizar a avaliação prática|
|**Objetivo**|Descrever como funciona a criação e disponibilização da avaliação prática em grupo|
|**Atores**|Professor|
|**Recursos**|Software|
|**Episódios**|O professor irá criar um pequeno contexto real de aplicação dos conhecimentos adquiridos com a preparação e avaliações para que o grupo possa resolver, o contexto será disponibilizado pelo professor no software durante a aula para os grupos de alunos aplicarem seus conhecimentos.|
 
### Cenário 13: Avaliação em pares
 
|||
|-----|-----|
|**Título**|Avaliação em pares|
|**Contexto**|Professor irá criar e disponibilizar a avaliação em pares|
|**Objetivo**|Descrever como funciona a criação e disponibilização da avaliação em pares aos alunos|
|**Atores**|Professor e Aluno|
|**Recursos**|Software|
|**Episódios**|Durante o semestre nas sessões do TBL o professor poderá disponibilizar uma avaliação em pares para que os alunos do grupo se avaliem, cada aluno irá distribuir 100 entre cada um dos membros do grupo e o porque dos pontos inseridos e falando o que devem melhorar, esses pontos vai somar a nota final de cada um dos alunos, esse feedback será disponibilizado para cada aluno em seu perfil, obviamente sem aparece quem mandou, o professor irá definir na criação da sessão se ele irá fazer essa avaliação e qual a porcentagem da nota ela terá.|
 
### Cenário 14: Notas e Rank
 
|||
|-----|-----|
|**Título**|Notas, rank|
|**Contexto**|O software irá disponibilizar as notas de cada aluno e o rank de grupos|
|**Objetivo**|Descrever como o software irá disponibilizar as notas de cada aluno e o rank de grupos|
|**Atores**|Professor e Aluno|
|**Recursos**|Software|
|**Episódios**|A cada sessão o software irá atualizar a planilha de notas de cada aluno com as notas (iRAT, gRAT, avaliação prática) e as notas do aluno avaliado pelos colegas se tiver, com isso ele irá calcular a média da turma e a nota da sessão do TBL de cada aluno pela matrícula dele, com isso o software irá disponibilizar o rank de grupos na qual o primeiro lugar ao final do semestre ficará no **hall da fama** para servir de exemplo nos próximos semestres para os próximos alunos, o rank de grupo será calculado pela média de notas das sessões de TBL de cada aluno do grupo, o grupo que tiver a maior média é o ganhador.|
 
### Cenário 15: Final do semestre
 
|||
|-----|-----|
|**Título**|Final do semestre|
|**Contexto**|As atividades finais do professor no final do semestre|
|**Objetivo**|Como realizar as atividades ao finalizar o semestre|
|**Atores**|Professor|
|**Recursos**|Software|
|**Episódios**|No final do semestre o professor irá retirar os alunos da turma para deixar vago novos alunos no próximo semestre e fechar a turma até que o semestre se inicie novamente, os alunos poderá entrar novamente na turma no próximo semestre se for o caso.|
