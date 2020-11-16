# <center> Requisitos

<div align="justify">

## 1. Introdução
Os requisitos foram elicitados utilizando mais de uma técnica de elicitação, de modo que foram dispostos em documentos separados. Todos os documentos foram analisados e comparados para que, ao final, pudesse ser feito um compilado dos requisitos, filtrados para que não houvesse repetição.

## 2. Metodologia
Os requisitos foram todos agrupados em única tabela para melhor visualização e também divididos em Requisitos Funcionais e Requisitos Não-funcionais. Segundo Bezerra (2007), os requisitos funcionais são aqueles que definem o comportamento do produto, as funcionalidades existentes, ou seja, é aquilo que descreve o que o sistema tem que fazer a cada ação de um usuário ou outro sistema. Já os requisitos não-funcionais são aqueles que descrevem as características que o sistema deve possuir, como padrões de desempenho, usabilidade, robustez, dentre outros.

## 3. Requisitos elicitados
**Total de requisitos**

|  ID  | <center> Descrição | <center>Prioridade |
|:----:|:-------------------|:--------------------|
| [ST01](/pages/elicitacao/storytelling#requisitos-storytelling-1)<br>[ST09](/pages/elicitacao/storytelling#requisitos-storytelling-4)<br>[ST06](/pages/elicitacao/storytelling#requisitos-storytelling-2) | O sistema deve ser capaz de salvar temporariamente os dados digitados pelo usuário quando estiverem dentro dos padrões | Must |
| [ST02](/pages/elicitacao/storytelling#requisitos-storytelling-1)<br>[ST10](/pages/elicitacao/storytelling#requisitos-storytelling-4)<br>[ST06](/pages/elicitacao/storytelling#requisitos-storytelling-2) | O sistema deve indicar as restrições nos campo de informação no momento em que o usuário inserir os dados | Must |
| [ST03](/pages/elicitacao/storytelling#requisitos-storytelling-1) | O sistema deve disponibilizar a rastreabilidade dos caminhos percorridos pelo usuário para que este possa se localizar a qualquer momento na página | Should |
| [ST04](/pages/elicitacao/storytelling#requisitos-storytelling-2) | O sistema deve informar quais campos são obrigatórios | Should |
| [ST05](/pages/elicitacao/storytelling#requisitos-storytelling-2) | Indicar com mais clareza o botão de criar exercícios | Could |
| [ST07](/pages/elicitacao/storytelling#requisitos-storytelling-3) | O sistema deve oferecer campo de ajuda ao longo da página | Must |
| [ST08](/pages/elicitacao/storytelling#requisitos-storytelling-3)<br>[ST12](/pages/elicitacao/storytelling#requisitos-storytelling-4) | O sistema deve permitir que o usuário cancele uma operação indesejada | Must |
| [ST11](/pages/elicitacao/storytelling#requisitos-storytelling-4) | O sistema deve reconhecer a extensão do arquivo inserido | Could |
| [INS01](/pages/elicitacao/introspeccao#requisitos-persona-1) | O sistema deve permitir que o professor visualize o grau de participação do aluno na plataforma | Could |
| [INS02](/pages/elicitacao/introspeccao#requisitos-persona-1) | O sistema deve possuir um chat acadêmico que possibilite a comunicação entre professor e aluno | Could |
| [INS03](/pages/elicitacao/introspeccao#requisitos-persona-1) | O sistema deve possuir uma área para que os usuários possam deixar sugestões de melhoria para a plataforma | Should |
| [INS04](/pages/elicitacao/introspeccao#requisitos-persona-2) |O sistema deve permitir integração com aplicativos externos |Could |
| [INS05](/pages/elicitacao/introspeccao#requisitos-persona-2) | O sistema deve exibir os resultados obtidos nos aplicativos externos e integrados | Could |
| [INS06](/pages/elicitacao/introspeccao#requisitos-persona-2) | O sistema deve permitir a inserção de vídeo-aulas na plataforma| Could|
| [INS07](/pages/elicitacao/introspeccao#requisitos-persona-3) | O sistema deve permitir alteração de idioma para uso da plataforma | Could |
| [INS08](/pages/elicitacao/introspeccao#requisitos-persona-3) | O sistema deve fornecer traduções consistentes para os conteúdos das páginas | Could |
| [INS09](/pages/elicitacao/introspeccao#requisitos-persona-3) | Deve ser possível adicionar comentário em textos traduzidos de forma inadequada | Could |
| [INS10](/pages/elicitacao/introspeccao#requisitos-persona-4) | O sistema deve possuir uma lista de aplicativos de possível integração com a plataforma | Could |
| [INS11](/pages/elicitacao/introspeccao#requisitos-persona-4) | O sistema deve permitir a correção de contests por juri-online | Could |
| [INS12](/pages/elicitacao/introspeccao#requisitos-persona-4) | O sistema deve permitir o cadastro em grupo de alunos para realização de um contest | Could |

**Requisitos Funcionais**

|  ID  | <center> Descrição | <center>Origem | Prioridade |
|:----:|:-------------------|:---------------|:----------:|
| RF01 | O sistema deve oferecer campo de ajuda ao longo da página | [ST07](/pages/elicitacao/storytelling#requisitos-storytelling-3) | Must |
| RF02 | O sistema deve permitir que o usuário cancele uma operação indesejada | [ST08](/pages/elicitacao/storytelling#requisitos-storytelling-3)<br>[ST12](/pages/elicitacao/storytelling#requisitos-storytelling-4) | Must |
| RF03 | O sistema deve permitir que o professor visualize o grau de participação do aluno na plataforma |[INS01](/pages/elicitacao/introspeccao#requisitos-persona-1) | Could |
| RF04 | O sistema deve possuir um chat acadêmico que possibilite a comunicação entre professor e aluno | [INS02](/pages/elicitacao/introspeccao#requisitos-persona-1) | Could |
| RF05 | O sistema deve possuir uma área para que os usuários possam deixar sugestões de melhoria para a plataforma | [INS03](/pages/elicitacao/introspeccao#requisitos-persona-1) | Could |
| RF06 | O sistema deve exibir os resultados obtidos nos aplicativos externos e integrados | [INS05](/pages/elicitacao/introspeccao#requisitos-persona-2) | Could |
| RF07 |  O sistema deve permitir a inserção de vídeo-aulas na plataforma | [INS06](/pages/elicitacao/introspeccao#requisitos-persona-2) | Could |
| RF08 | O sistema deve permitir alteração de idioma para uso da plataforma | [INS07](/pages/elicitacao/introspeccao#requisitos-persona-3) | Could |
| RF09 | Deve ser possível adicionar comentário em textos traduzidos de forma inadequada | [INS09](/pages/elicitacao/introspeccao#requisitos-persona-3) | Could |
| RF10 | O sistema deve possuir uma lista de aplicativos de possível integração com a plataforma | [INS10](/pages/elicitacao/introspeccao#requisitos-persona-4) | Could |
| RF11 | O sistema deve permitir a correção de contests por juri-online | [INS11](/pages/elicitacao/introspeccao#requisitos-persona-4) | Could |
| RF12 | O sistema deve permitir o cadastro em grupo de alunos para realização de um contest | [INS12](/pages/elicitacao/introspeccao#requisitos-persona-4) | Could |
  
**Requisitos Não-Funcionais**

|  ID  | <center> Descrição | <center>Origem | Prioridade |
|:----:|:-------------------|:---------------|:----------:|
| RNF01 | O sistema deve ser capaz de salvar temporariamente os dados digitados pelo usuário quando estes estiverem dentro dos padrões | [ST01](/pages/elicitacao/storytelling#requisitos-storytelling-1)<br>[ST09](/pages/elicitacao/storytelling#requisitos-storytelling-4) | Must|
| RNF02 | O sistema deve indicar as restrições nos campo de informação no momento em que o usuário inserir os dados | [ST02](/pages/elicitacao/storytelling#requisitos-storytelling-1)<br>[ST10](/pages/elicitacao/storytelling#requisitos-storytelling-4) | Must | 
| RNF03 | O sistema deve disponibilizar a rastreabilidade dos caminhos percorridos pelo usuário para que este possa se localizar a qualquer momento na página | [ST03](/pages/elicitacao/storytelling#requisitos-storytelling-1) | Should | 
| RNF04 | O sistema deve informar quais campos são obrigatórios |  [ST04](/pages/elicitacao/storytelling#requisitos-storytelling-2) | Should | 
| RNF05 | Indicar com mais clareza o botão de criar exercícios | [ST05](/pages/elicitacao/storytelling#requisitos-storytelling-2) | Could | 
| RNF06 | O sistema deve reconhecer a extensão do arquivo inserido |  [ST11](/pages/elicitacao/storytelling#requisitos-storytelling-4) | Could | 
| RNF07 | O sistema deve permitir integração com aplicativos externos | [INS04](/pages/elicitacao/introspeccao#requisitos-persona-2) | Could | 
| RNF08 | O sistema deve fornecer traduções consistentes para os conteúdos das páginas | [INS08](/pages/elicitacao/introspeccao#requisitos-persona-3) | Could |

</div>

## Bibliografia
BEZERRA, Eduardo. **Princípios de análise e projeto de sistema com UML**. Rio de Janeiro, Elsevier, 2007.
