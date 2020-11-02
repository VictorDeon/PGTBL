# <center>Storytelling

<div align="justify">

## 1. Introdução

O método de elicitação chamado de _storytelling_ trabalha a ideia de adquirir conhecimento por meio de histórias, sejam elas contadas por um grupo de pessoas ou até mesmo uma organização. É o compartilhamento de conhecimento por meio da narração de histórias em grupo a respeito da experiência de cada narrador ao utilizar o sistema. Neste projeto, cada integrante do grupo utilizou a plataforma PGTBL e, assim, foram gerados os relatos descritos ao longo deste documento juntamente com tabelas contendo os requisitos extraídos neste processo. 

## 2. Metodologia
A elicitação dos requisitos será feita por meio do método de _storytelling_ que permite entendimento a respeito do contexto de uso do usuário, as tarefas realizadas e, assim, a elicitação dos requisitos necessários para aquele objetivo narrado. Além de documentados, os requisitos foram priorizados utilizando a técnica MoSCoW (Must, Should, Could, Won't).

Essa técnica de priorizaçao consiste em classificar o grau de importância dos requisitos, onde usa-se "Must" para requisitos de caráter mandatório para o projeto continuar; "Should" para requisitos que não são essenciais para o funcionamento do sistema mas deixariam a plicação muito melhor; "Could" para requisitos que seriam desejáveis mas não obrigatórios; e "Won't" para requisitos que não são prioridade no momento.

## Storytelling 1 - Criação de disciplinas
Este storytelling tem o objetivo de identificar como um usuário em perfil de professor realiza as tarefas para alcançar o objetivo de criação de uma disciplina.

**Rastreabilidade**

| Nome               | Papel     | Observação                |
|:-------------------|:----------|:--------------------------|
| Rafaella Junqueira | Narração  | Membro da equipe/ Usuário |
| Ingrid Soares      | Relatório | Membro da equipe          |

**Resumo da narração**

O usuário começou a utilizar a plataforma com o perfil de professor e, ao tentar criar uma disciplina, notou que somente após inserir todas as informações necessárias e tentar finalizar a criação da disciplina é que a plataforma informou algumas limitações aos campos de "título da sala" e "limite de estudantes". Então, todas as informações foram apagadas, inclusive as que estavam de acordo com o padrão exigido, de tal forma que, caso ocorresse algum outro erro, tudo deveria ser digitado novamente. 

Após uma série de tentativas para definir um nome para a "sala de aula", descobriu que o mesmo deveria iniciar com a palavra "class" e que o campo de monitores também possuia um limite não especificado no momento em que um valor era inserido. Criada a disciplina, o usuário voltou à página de perfil para visualizar as disciplinas criadas e percebeu não saber se estava visualizando "todas as disciplinas" ou as "disciplinas criadas". No momento em que foi visualizar 

**Requisitos elicitados**

| ID   | Descrição           | Prioridade     |
|:-----|:--------------------|:--------------:|
| ST01 | O sistema deve ser capaz de salvar temporariamente os dados digitados pelo usuário quando estes estiverem dentro dos padrões | Must |
| ST02 | O sistema deve indicar as restrições nos campo de informação no momento em que o usuário inserir os dados | Should |
| ST03 | O sistema deve disponibilizar a rastreabilidade dos caminhos percorridos pelo usuário para que este possa se localizar a qualquer momento na página  | Should |

## Storytelling 2 - Criação de exercícios na Seção TBL
Este storytelling tem o objetivo de identificar como um usuário em perfil de professor realiza as tarefas para alcançar o objetivo de criar um exercício na seção TBL.

**Rastreabilidade**

| Nome               | Papel     | Observação                |
|:-------------------|:----------|:--------------------------|
| João Victor Matos  | Narração  | Membro da equipe/ Usuário |
| Rafaella Junqueira | Relatório | Membro da equipe          |

**Resumo da narração**

O usuário ao utilizar a plataforma com perfil de professor, após conseguir criar uma disciplina e criar uma sessão TBL, ao tentar criar um exercicio percebeu que não possuia uma indicação clara sobre o local na plataforma onde são criadas as exercícios. O que existe é apenas um botão com um sinal de mais e, mesmo após acessada a área correta, não são informados quais campos são obrigatórios e as restrições de limite de dados exigidas por cada campo.     

Também foi observado que ao criar um exercício sem marcar a alternativa correta o sistema avisa esse erro, porém, a opção de marcar qual alternativa esta correta torna-se indisponível logo em seguida, obrigando ao usuário ter que voltar para a lista de exercícios e reiniciar o processo de criação de um exercício, perdendo as informações anteriormente inseridas. 


**Requisitos elicitados**

| ID   | Descrição                                             | Prioridade     |
|:-----|:------------------------------------------------------|:--------------:|
| ST04 | O sistema deve informar quais campos são obrigatórios | Should         |
| ST05 | Indicar com mais clareza o botão de criar exercícios  | Could          |
| ST06 | O sistema deve permitir selecionar qual é a alternativa correta mesmo após erro de não ter selecionado antes | Should |

## Storytelling 3 - Criação de turma
Este storytelling tem o objetivo de identificar como um usuário em perfil de professor realiza as tarefas para alcançar o objetivo de criação de uma turma.

**Rastreabilidade**

| Nome               | Papel     | Observação                |
|:-------------------|:----------|:--------------------------|
| Ingrid Soares      | Narração  | Membro da equipe/ Usuário |
| João Victor Matos  | Relatório | Membro da equipe          |

**Resumo da narração**
<!-- Coloque aqui sua narração -->
<!-- Não esquecer de seguir a numeração anterior -->
<!-- Coloque seu nome na tabela de versionamento ao final -->
**Requisitos elicitados**

| ID         | Descrição           | Prioridade     |
|:-----------|:--------------------|:--------------:|
| ST0X       |                     |                |





</div>

## Bibliografia
**Técnica de priorização MoSCoW**. Disponível em https://rockcontent.com/br/blog/metodo-moscow/#:~:text=O%20m%C3%A9todo%20MoSCoW%20%C3%A9%20uma,elas%20atribuem%20a%20cada%20requisito. Acesso em 31 de outubro de 2020.

PMBOK, GUIA. **Um guia do conjunto de conhecimentos em gerenciamento de projetos.** Project Management Institute. 2004.


#### Histórico de Versão
| Data       | Versão | Descrição                  | Autor(es)          |
|:----------:|:------:|:--------------------------:|:------------------:|
| 31.10.2020 | 0.1    | Criação do documento       | Rafaella Junqueira |
| 01.11.2020 | 0.2    | Adição storytelling 2       | João Victor |
