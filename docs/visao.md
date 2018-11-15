# Visão do produto PGTBL
***
## 1. Introdução
***

Este documento tem como objetivo definir o que é a plataforma TBL, bem como suas aplicações e funcionalidades. Para isso, será feito um detalhamento do projeto, citando as inovações que a plataforma oferece.
 
Dessa maneira, visa-se que o leitor, seja ele usuário do sistema ou um investidor, consiga entender a proposta da plataforma, além das funcionalidades oferecidas.
 
[Canvas de projeto](canvas)
 
### 1.1 Finalidade
 
O projeto TBL ou Team Based Learning é um modelo educacional já empregado em várias universidades que modifica a forma de aprendizado e avaliação tradicional, que ainda é empregado em muitas universidade e escolas. A finalidade do software é que a aplicação do TBL se torne algo mais fácil e constante, tornando o processo mais prazeroso, tanto para o aluno quanto para o professor através dessa tecnologia.
 
### 1.2 Escopo
 
O objetivo inicial do projeto é a aplicação do software em disciplinas da UnB, substituído o método tradicional de ensino e avaliação, tornando o processo mais prazeroso, tanto para o aluno quanto para o professor através dessa tecnologia.
 
O sistema terá um design atrativo e será responsável por todo o processo do TBL desde a preparação até a avaliação em pares. Futuramente a aplicação terá um sistema de machine learning e Gamificação além de ser extensível a qualquer disciplina ou curso tanto superior como ensino médio.
 
### 1.3 Visão Geral
 
O documento está organizado de maneira que o leitor consiga extrair o máximo de informações possíveis, de forma coesa. Para isso, primeiramente são mostradas as necessidades e motivações que levaram à criação do software. Após isso, são detalhados os aspectos referentes aos envolvidos no projeto, definindo a equipe de desenvolvimento e a de gestão, além de apresentar como o software afetará os usuários. Concluindo, são apresentados os recursos e as funcionalidades que o software possuirá, entre outras coisas.
 
### 1.4 Definições, Acrônimos e Abreviações
 
A maioria das definições relacionadas ao software se encontra na página: [Léxicos](lexicos)
 
* **TBL**: Team-based Learning.
* **UnB**: Universidade de Brasília, Brasil.
* **RAT**: Radiness Assurance Test ou Garantia de preparo
* **iRAT**: Individual Readiness Assurance Test
* **gRAT**: Group Readiness Assurance Test
* **FGA:** Faculdade do Gama, campus de engenharia da UnB.
 
***
## 2. Posicionamento
***

### 2.1 Oportunidade de negócio
 
Inicialmente o software vai ser voltado para fins educacionais, sendo implantado em universidades e colégios públicos, pois o TBL cria uma barreira que deve ser quebrada, que é sair do comodismo da avaliação e ensino tradicional, ou seja, provas e slides, e substituir pelo modelo de ensino baseado em equipes ou Team Based Learning que irá fazer o aluno estudar de maneira constante durante todo o semestre.
 
### 2.2 Descrição do problema
 
![fishbone](https://user-images.githubusercontent.com/14116020/38155591-fc6ed9f8-344e-11e8-894c-8a95c51974a9.png)
 
<table>
  <tr>
    <td colspan="2"><b>Descrição do problema</b></td>
  </tr>
  <tr>
    <td>O problema seria</td>
    <td>forma tradicional de ensino e avaliação do conhecimento do aluno.</td>
  </tr>
  <tr>
    <td>que afeta</td>
    <td>futuros profissionais.</td>
  </tr>
  <tr>
    <td>cujo impacto é</td>
    <td>Os alunos não se motivam a aprender, eles apenas buscam um diploma, aumentando o índice de desigualdade social e gerando profissionais pouco preparados para o mercado de trabalho.</td>
  </tr>
  <tr>
    <td>e uma boa solução seria</td>
    <td>de forma simples e com um design atrativo e gamificado, criar uma plataforma para que as escolas e universidades possa modificar a forma de ensino e avaliação tendo a participação ativa dos alunos, gerando profissionais capacitados e que saibam trabalhar em equipe.</td>
  </tr>
</table>
 
### 2.3 Declaração da Posição do Produto
 
<table>
  <tr>
    <td colspan="2"><b>Declaração da Posição do Produto</b></td>
  </tr>
  <tr>
    <td>Para</td>
    <td>instituições</td>
  </tr>
  <tr>
    <td>que</td>
    <td>desejam melhorar a forma de ensino e aprendizado, motivando os alunos a participarem mais das aulas, estudarem com mais constância e aprenderem a trabalhar em equipe</td>
  </tr>
  <tr>
    <td>O TBL</td>
    <td>é um sistema web</td>
  </tr>
  <tr>
    <td>Que</td>
    <td>torna possível a aplicação do modelo de Team Based Learning em universidade e escolas que desejam melhorar a educação de seus alunos.</td>
  </tr>
  <tr>
    <td>Diferente de</td>
    <td>outras formas de avaliação como provas e trabalhos</td>
  </tr>
  <tr>
    <td>Nosso produto</td>
    <td>Visa tornar o ensino algo mais prazeroso para o professor e para o aluno, preparando ele para o mercado de trabalho.</td>
  </tr>
</table>
 
***
## 3. Descrição dos Envolvidos e dos Usuários
***
 
### 3.1 Resumo dos Envolvidos
 
|Nome|Descrição|Responsabilidade|Representante|
|:---|:-------|:----------------|:------------|
|Scrum master|Gerenciam o projeto e a equipe|Elaboram os planos de projeto, Monitoram o andamento do projeto, Revisam o projeto, Auxiliam a equipe de desenvolvimento a seguir a metodologia|Victor Arnaud|
|Time|Desenvolvem o sistema|Documentação, código e testes|Victor Arnaud|
|Product owner|Requisitou o sistema|Fornece e valida os requisitos do sistema, avalia o andamento do produto a cada release e tem um acompanhamento constante do projeto.|Elaine Venson, Cristiane Soares Ramos, Ricardo Ajax|
 
### 3.2 Resumo dos Usuários
 
|Nome|Descrição|
|:---|:-------|
|Professor|Pessoas que procuram um meio para melhorar o ensino e preparar seus alunos para o mercado.|
|Alunos|Pessoas que procurar aperfeiçoar seus conhecimento e se preparar para o mercado|
 
### 3.3 Perfis dos Usuários
 
<table>
  <tr>
    <td colspan="2"><b>Professores.</b></td>
  </tr>
  <tr>
    <td>Representantes:</td>
    <td>Professores</td>
  </tr>
  <tr>
    <td>Descrição:</td>
    <td>Pessoas que busca melhorar o ensino e a forma de avaliação das escolas e universidades.</td>
  </tr>
  <tr>
    <td>Responsabilidades:</td>
    <td>gerenciamento das disciplinas e alunos usando o sistema baseado no TBL. O professor também é responsável por criar e gerenciar listas e avaliações.</td>
  </tr>
  <tr>
    <td>Critérios de Sucesso:</td>
    <td>Permite que os alunos possam aprender de uma maneira mais ativa e colaborativa</td>
  </tr>
  <tr>
    <td>Envolvimento:</td>
    <td>Alto</td>
  </tr>
</table>
 
<table>
  <tr>
    <td colspan="2"><b>Alunos.</b></td>
  </tr>
  <tr>
    <td>Representantes:</td>
    <td>Alunos</td>
  </tr>
  <tr>
    <td>Descrição:</td>
    <td>Pessoas que queiram aprender e se preparar para o mercado de trabalho de forma colaborativa e não competitiva</td>
  </tr>
  <tr>
    <td>Responsabilidades:</td>
    <td>Fazer todas as atividades relacionadas ao TBL.</td>
  </tr>
  <tr>
    <td>Critérios de Sucesso:</td>
    <td>Aprender as disciplinas e se sentir preparado para atuar no mercado.</td>
  </tr>
  <tr>
    <td>Envolvimento:</td>
    <td>Alto</td>
  </tr>
</table>
 
### 3.5 Principais necessidades dos usuários ou dos envolvidos
 
|Necessidade|Prioridade|Preocupações|Solução Proposta|Solução Atual|
|:----------|:--------:|:-----------|:---------------|:------------|
|Gerenciar as aulas|Alta|Consegui gerenciar as aulas através do TBL|Software que ajude na aplicação da metodologia|Ensino com pouca participação do aluno e avaliação ineficiente do conhecimento dos alunos.|
|Aprender disciplinas|Alta|Os alunos devem sair das universidades preparados para o mercado de trabalho e das escolas preparados para a universidade|Software que faça o aluno ser mais ativo nas aulas e aprenda a trabalhar em equipe|Alunos pouco preparados para o mercado de trabalho|
 
###  3.6 Alternativas e concorrência
 
Não foi encontrada nenhum site que automatiza as tarefas do Team Based Learning, apenas artigos, livros e sites ensinando como aplicar o TBL dentro das universidades e escolas usando apenas papel e caneta.

* [Moodle](https://aprender.unb.br/): Mesmo que siga a mesma ideia do software proposto o moodle normalmente serve só para disponibilizar informações e arquivos relevantes para os alunos.

* [Blackboard IESB](https://iesb.blackboard.com/): Também segue a mesma ideia, mas não aplica conceitos do Team Based Learning

***
## 4. Visão Geral do Produto
***

### 4.1 Perspectiva do produto
 
Este sistema tem como objetivo inovar a forma como as escolas/universidades ensinam seus alunos através do TBL, fazendo com que eles tenham uma preparação mais adequada para atuar no mercado, tendo a participação ativa dos alunos e aprimorando seu trabalho em equipe.
 
### 4.2. Recursos do Produto
 
Nesta seção, os recursos do sistema serão descritos usando uma abordagem de alto nível.

|Recurso|Descrição|
|:-----:|:--------|
|Administrar Disciplinas e alunos|O professor pode adicionar, remover, criar e editar disciplinas e turmas e disponibilizar a senha de acesso a elas para os alunos entrarem, além de poder remover ou adicionar estudantes na turma e gerenciar suas notas.|
|Criar conta|O professor e os alunos pode criar sua contas no sistema, apenas passando seus dados pessoais como nome, email, senha, e usuário|
|Gerenciar dados pessoais|O usuário poderá editar sua senha e dados pessoais do usuário conforme necessário.|
|Funcionalidades do TBL|Funcionalidades relacionadas às fases de preparação, garantia de preparo ou RAT, iRAT, gRAT e apelações, Aplicação de conceitos e avaliação em pares|
|Relatório|O professor terá um dashboard com relatórios do desempenho dos alunos em cada questão da avaliação, tendo um feedback para o que ele deve focar mais nas aulas.|
|Rank e Gamificação|Terá também um rank de grupos, na qual o primeiro colocado ficará exposto no **Hall da Fama** que será visto por novos alunos dos próximos semestres, não há rank individual porque o objetivo não é a competição e sim a colaboração.|
 
***
## 5. Restrições
***
 
### 5.1 Restrições de implementação
 
A proposta do serviço ofertado que é abrangida nesse documento, envolve a utilização de certos recursos que necessitam de um navegador. De modo que tais recursos implicam em certas limitações do produto, estas limitações seriam:
 
* O usuário deve dispor de um provedor de internet;
* O usuário deve dispor de um navegador;
 
### 5.2 Restrições de confiabilidade
 
O sistema deve ter cobertura de testes - mínimo de 90%;
 
***
## 6. Requisitos de Qualidade
***

**Sistema**: O sistema deve seguir a arquitetura MVC definida no [documento de arquitetura](contribuicao/arquitetura) e as ferramentas de desenvolvimento será o Python (versão 3.5) e o framework Django (versão 2.0).

**Suportabilidade**: O sistema poderá ser acessado em computadores pessoais - notebook, desktop – utilizando-se de um serviço de internet. Sendo uma aplicação Web compatível com os principais sistemas operacionais (Linux, Mac, Windows), acessada através do navegador Google Chrome e/ou Firefox de um dispositivo móvel ou fixo.
 
**Qualidade**: O sistema deve seguir uma folha de estilo a ponto de o código ser legivel e de fácil manutenção, tendo como base boas práticas de programação, o sistema deve ter baixo acoplamento e alta coesão além de ser modularizado focando na flexibilidade e manutenção do mesmo.

**Usabilidade**: O sistema deve ser responsivo, adaptando-se à plataforma que o usuário estiver utilizando e o design deve ser fácil de usar e aprender e seguir todos as heurísticas de usabilidade.

**Desempenho**:  Por ser um sistema web o software necessita de uma conexão estável com a internet para seu funcionamento. A velocidade da internet tem impacto direto no desempenho da aplicação, sendo necessário uma velocidade suficiente para processar as informações e executar as funcionalidades do sistema.
 
**Segurança**: O sistema deve apresentar uma boa percentagem de cobertura de testes e bastante encapsulamento de código, além de um sistema de log eficiênte e ter confiabilidade..

**Confiabilidade**:  O sistema deve se comprometer em apresentar informações confiáveis para o usuário do sistema, entretanto dependerá diretamente dos demais usuários, uma vez que o conteúdo apresentado será de autoria destes e deve apresentar um sistema de autenticação, autorização e recuperação seguro e eficiente.
