# <center>Introspecção

<div align="justify">

## 1. Introdução
A técnica de introspecção se baseia em imaginar que tipo de sistema seria desejável por uma pessoa ao executar determinada tarefa utilizando um esquipamento específico, em um local específico, entre outros. Ou seja, o profissional da Engenharia de Requisitos deve imaginar o que gostaria que existisse no produto caso tivesse que desempenhar uma dada tarefa, com os equipamentos disponíveis no momento. Essa técnica auxiliar na identificação das propriedades que o sistema deve possuir para que atenda as necessidades do seu público alvo.

## 2. Objetivo
Este documento tem a finalidade de apresentar os requisitos funcionais elicitados pela técnica de introspecção e, posteriormente, contribuir com a elicitação geral dos requisitos deste projeto.

## 3. Metodologia
O analista de requisitos busca por histórias de usuário baseadas no que ele imagina que os usuarios do sistema precisam que seja fornecido pelo software separando tais necessidades por prioridades (MoSCoW). Para documentar as introspecções foram criadas personas que representam usuários típicos da plataforma, e são definidas principalmente por seus objetivos. 

## 4. Introspecção
<b>Personas</b><br>
A partir de uma visão geral do produto e a fim de propor situações diferentes do previsto em um cenário comum de possibilidades, as personas aparecerem para se relacionarem com algum tipo de envolvimento, no contexto de requisitos, com o PGTBL, sendo esse contato direto ou não. A prioridade MoSCoW também será determinada de acordo com as necessidades da persona em questão.

Exemplo de situações "comuns"
<table role="table">
<thead>
<tr>
<th align="left">ID</th>
<th align="left">Requisito</th>
<th align="left">Prioridade</th>
</tr>
</thead>
<tbody>
<tr>
<td align="left"><code>1</code></td>
<td align="left">Deve ser possível gerenciar as aulas através do TBL</td>
<td align="left">Must</td>
</tr>
<tr>
<td align="left"><code>2</code></td>
<td align="left">Deve ser possível qualificar os alunos para o mercado de trabalho</td>
<td align="left">Must</td>
</tr>
<tr>
<td align="left"><code>3</code></td>
<td align="left">Deve ser possível aos professores e alunos alterar dados cadastrais</td>
<td align="left">Should</td>
</tr>
<tr>
<td align="left"><code>3</code></td>
<td align="left">Deve ser possível aos professores administrar suas disciplinas e seus alunos</td>
<td align="left">Should</td>
</tr>
 <tr>
<td align="left"><code>4</code></td>
<td align="left">Deve ser possível aos professores visualizar relatório dos alunos e realizar feedback</td>
<td align="left">Should</td>
</tr>
</tbody>
</table>

<h4 id="persona-1-caroline">Persona 1 - Caroline</h4>
<table>
<thead>
<tr>
<th><strong>Persona 1 </strong></th>
<th><strong>Caroline</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Nome:</strong></td>
<td>Caroline</td>
</tr>
<tr>
<td><strong>Profissão:</strong></td>
<td>Professora de Comunicação da UnB.</td>
</tr>
<tr>
<td><strong>Escolaridade:</strong></td>
<td>Formada em Comunicação, Doutorado em Design.</td>
</tr>
<tr>
<td><strong>Nível de conhecimento sobre o app:</strong></td>
<td>Acabou de instalar a aplicação e não tem costume de ter auxílio de ferramentas para lecionar aulas, apesar de ter um conhecimento prévio sobre programação front-end.</td>
</tr>
<tr>
<td><strong>Intenção ao usar o aplicativo:</strong></td>
<td>Utilizar a ferramenta para gerenciar programação de aulas, interação com alunos e obter relatórios dos alunos de modo mais dinâmico para possibilitar às suas turmas gerar resultados mais satisfatórios à partir de meios virtuais.</td>
</tr>
<tr>
<td><strong>História e contexto:</strong></td>
<td> Caroline gostou da função da plataforma, do seu design intuitivo e de suas funcionalidades. Também gostou da ideia de observar os alunos estudarem colaborativamente e obterem resultados em equipe, e acredita que assim possibilitará que seus alunos sejam mais ativos durante das aulas e agirá de maneira mais organizada em prol do seu resultado das suas classes, uma vez que isso refletirá diretamente em seu desempenho, além de ter como gerenciar o desempenho da turma por meio de relatórios, feedbacks e rankings. Ela acredita que isso pode interferir diretamente na forma que serão preparados para o mercado de trabalho.</td>
</tr>
<tr>
<td><strong>O que ele acha que poderia mudar:</strong></td>
<td>Caroline gostaria que seus alunos também pudessem visualizar rankings individuais para fins de evolução pessoal, apesar de ter achado muito interessante os rankings somente no modo coletivo, e relatórios de desempenho no dashboard dos professores. Ela também gostaria que houvessem mais funcionalidades que integrassem os alunos, como um chat direcionado para assuntos acadêmicos, e um espaço destinado à sugestões para melhoria da ferramenta.</td>
</tr>
</tbody>
</table>

#### Requisitos - Persona 1
<table>
<thead>
<tr>
<th>Código</th>
<th>Descrição</th>
<th>Prioridade</th>
</tr>
</thead>
<tbody>
<tr>
<td>INS01</td>
<td>O sistema deve permitir que o professor visualize o grau de participação do aluno na plataforma</td>
<td>Could   </td>
</tr>
<tr>
<td>INS02</td>
<td>O sistema deve possuir um chat acadêmico que possibilite a comunicação entre professor e aluno</td>
<td>Could   </td>
</tr>
<tr>
<td>INS03</td>
<td>O sistema deve possuir uma área para que os usuários possam deixar sugestões de melhoria para a plataforma</td>
<td>Should   </td>
</tr>
</tbody>
</table>
<hr />

<h4 id="persona-2-carlos">Persona 2 - Douglas</h4>
<table>
<thead>
<tr>
<th><strong>Persona 2 </strong></th>
<th><strong>Douglas</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Nome:</strong></td>
<td>Douglas</td>
</tr>
<tr>
<td><strong>Profissão:</strong></td>
<td>Professor de Educação Física da UnB.</td>
</tr>
<tr>
<td><strong>Escolaridade:</strong></td>
<td>Formado em Educação Física.</td>
</tr>
<tr>
<td><strong>Nível de conhecimento sobre o app:</strong></td>
<td>Possui apenas conhecimento intuitivo sobre como utilizar a aplicação, por ter outros tipos de aplicativos direcionados para treino pessoal e de alunos.</td>
</tr>
<tr>
<td><strong>Intenção ao usar o aplicativo:</strong></td>
<td>Facilitar a comunicação à distância e também diariamente com os alunos, e também entre eles.</td>
</tr>
<tr>
<td><strong>História e contexto:</strong></td>
<td> Douglas teve dificuldade de se acostumar com o aplicativo para suprir todas as necessidades ao longo da sua disciplina, que por mais que tenha hábito de uso de plataformas digitais, para lecionar aulas tem mais hábito e facilidade de gerenciar uma turma de modo presencial, algumas vezes fazendo uso do Moodle para principalmente disponibilizar o cronograma do semestre aos seus alunos e também fazendo uso de outros aplicativos relacionados à sua matéria. A interação e o "espírito de equipe" entre os alunos já acontecia durante suas aulas, então em relação à isso não sentiu muita necessidade de interação virtual entre a sua turma.</td>
</tr>
<tr>
<td><strong>O que ele acha que poderia mudar:</strong></td>
<td>Integração com aplicativos de atividade física. Possibilidade de obter resultados associados aos aplicativos integrados. Permitir que os alunos sugiram melhorias no formato de aulas decidido pelo professor.</td>
</tr>
</tbody>
</table>

#### Requisitos - Persona 2
<table>
<thead>
<tr>
<th>Código</th>
<th>Descrição</th>
<th>Prioridade</th>
</tr>
</thead>
<tbody>
<tr>
<td>INS04</td>
<td>O sistema deve permitir integração com aplicativos externos</td>
<td>Could   </td>
</tr>
<tr>
<td>INS05</td>
<td>O sistema deve exibir os resultados obtidos nos aplicativos externos e integrados</td>
<td>Could   </td>
</tr>
<tr>
<td>INS06</td>
<td> O sistema deve permitir a inserção de vídeo-aulas na plataforma</td>
<td>Could   </td>
</tr>
</tbody>
</table>
<hr />


<h4 id="persona-3-Miguel">Persona 3 - Miguel</h4>
<table>
<thead>
<tr>
<th><strong>Persona 3 </strong></th>
<th><strong>Miguel</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Nome:</strong></td>
<td>Miguel</td>
</tr>
<tr>
<td><strong>Profissão:</strong></td>
<td>Professor de Espanhol da UnB.</td>
</tr>
<tr>
<td><strong>Escolaridade:</strong></td>
<td>Formado em pedagogia. Nacionalidade Argentina.</td>
</tr>
<tr>
<td><strong>Nível de conhecimento sobre o app:</strong></td>
<td>Possui apenas conhecimento intuitivo sobre como utilizar a aplicação.</td>
</tr>
<tr>
<td><strong>Intenção ao usar o aplicativo:</strong></td>
<td>Gerenciar suas turmas por meio do aplicativo.</td>
</tr>
<tr>
<td><strong>História e contexto:</strong></td>
<td> Miguel gostou da ideia, mas teve dificuldade de se adaptar, porque como ele não dá apenas aula do seu idioma e por ter dificuldade com a lingua portuguesa, seus alunos das disciplinas de pedagogia não conseguem acompanhar muito bem seus métodos e acabam com algumas dificuldade de como proceder em relação à algumas atividades.</td>
</tr>
<tr>
<td><strong>O que ele acha que poderia mudar:</strong></td>
<td>Alteração de idiomas para uso pessoal do aplicativo e traduções mais precisas para o professor e seus alunos. Alunos sugerirem edições às traduções e métodos.</td>
</tr>
</tbody>
</table>

#### Requisitos - Persona 3
<table>
<thead>
<tr>
<th>Código</th>
<th>Descrição</th>
<th>Prioridade</th>
</tr>
</thead>
<tbody>
<tr>
<td>INS07</td>
<td>O sistema deve permitir alteração de idioma para uso da plataforma</td>
<td>Could</td>
</tr>
<tr>
<td>INS08</td>
<td>O sistema deve fornecer traduções consistentes para os conteúdos das páginas</td>
<td>Could</td>
</tr>
<tr>
<td>INS09</td>
<td>Deve ser possível adicionar comentário em textos traduzidos de forma inadequada</td>
<td>Could</td>
</tr>
</tbody>
</table>
<hr />

<h4 id="persona-4-Miguel">Persona 4 - Otávio</h4>
<table>
<thead>
<tr>
<th><strong>Persona 4 </strong></th>
<th><strong>Otávio</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Nome:</strong></td>
<td>Otávio</td>
</tr>
<tr>
<td><strong>Profissão:</strong></td>
<td>Professor de Ciencia da Computação da UnB.</td>
</tr>
<tr>
<td><strong>Escolaridade:</strong></td>
<td>Formado em Ciencia da computação.</td>
</tr>
<tr>
<td><strong>Nível de conhecimento sobre o app:</strong></td>
<td>Possui apenas conhecimento técnico sobre como utilizar a aplicação.</td>
</tr>
<tr>
<td><strong>Intenção ao usar o aplicativo:</strong></td>
<td>Gerenciar suas turmas por meio do aplicativo e promover dinâmicas para seus alunos, divididos por grupos.</td>
</tr>
<tr>
<td><strong>História e contexto:</strong></td>
<td> Otávio gostou muito da ideia e também teve facilidade de adaptação. Acredita que possibilitará um resultado muito efetivo para os alunos nas disciplinas que ministra, principalmente em matérias com demandas constantes, quando comparado às matérias mais teóricas ou mais iniciantes, palestras etc.</td>
</tr>
<tr>
<td><strong>O que ele acha que poderia mudar:</strong></td>
<td>Possibilitar que professores sugiram para suas matérias integração com aplicativos, ou uma seção que possibilite visualizar aplicativos já previamente selecionados para integrarem com a aplicação em questão. Permitir sugestão de melhorias por parte de alunos e professores. Visualização individual dos rankings dos alunos, sem fins de competição.</td>
</tr>
</tbody>
</table>

#### Requisitos - Persona 4
<table>
<thead>
<tr>
<th>Código</th>
<th>Descrição</th>
<th>Prioridade</th>
</tr>
</thead>
<tbody>
<tr>
<td>INS10</td>
<td>O sistema deve possuir uma lista de aplicativos de possível integração com a plataforma</td>
<td>Could   </td>
</tr>
<tr>
<td>INS11</td>
<td>O sistema deve permitir a correção de contests por juri-online </td>
<td>Could </td>
</tr>
<tr>
<td>INS12</td>
<td>O sistema deve permitir o cadastro em grupo de alunos para realização de um contest</td>
<td>Could</td>
</tr>
</tbody>
</table>
<hr />

</div>

## Bibliografia
**Tese sobre Introspecção**. Disponível em http://www2.dbd.puc-rio.br/pergamum/tesesabertas

**Técnica de priorização MoSCoW** Disponível em https://www.fm2s.com.br/metodo-moscow/ Acesso em 9 de novembro de 2020.

#### Histórico de Versão
| Data       | Versão | Descrição                  | Autor(es)          |
|:----------:|:------:|:--------------------------:|:------------------:|
| 08.11.2020 | 0.1    | Criação do documento       | Ingrid Soares |
| 10.11.2020 | 0.1    | Revisão do documento       | Rafaella Junqueira |
