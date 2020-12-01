# <center> Matriz de rastreabilidade

<div align="justify">

## 1. Introdução 

A rastreabilidade de requisitos pode ser vista como a habilidade de acompanhar e descrever a vida de um requisito. A pós-rastreabilidade é uma característica de sistemas nos quais requisitos são claramente ligados às fontes e aos artefatos criados. Esta matriz Backward From busca ligar cada requisito levantado, artefatos de desenho e implementação de volta aos respectivos métodos de elicitação e modelagem utilizados neste projeto. (LEITE, 2005)

## 2. Legendas

| Código | <center>Significado              | Etapa relacionada   |
|:------:|:---------------------------------|:--------------------|
| RP     | Rich Picture                     | Pré-rastreabilidade |
| ST     | Storytelling                     | Elicitação          |
| INS    | Introspecção                     | Elicitação          |
| RF     | Requisito Funcional              | Elicitação          |
| RNF    | Requisito não funcional          | Elicitação          |
| CN     | Característica de Negócio        | Elicitação          |
| L      | Léxico                           | Modelagem           |
| EP     | Épico                            | Modelagem           |
| US     | User Story (História de Usuário) | Modelagem           |

## 3. Matriz Backward From
| Código | <center>Descrição | Elicitação | Modelagem |
|:------:|:----------|:-----------|:----------|
| RF01 | O sistema deve oferecer campo de ajuda ao longo da página | [ST07](/pages/elicitacao/storytelling#requisitos-storytelling-3) | L20, US28 | 
| RF02 | O sistema deve permitir que o usuário cancele uma operação indesejada | [ST08](/pages/elicitacao/storytelling#requisitos-storytelling-3)<br>[ST12](/pages/elicitacao/storytelling#requisitos-storytelling-4) | L7, L10, L11, US11 |
| RF03 | O sistema deve permitir que o professor visualize o grau de participação do aluno na plataforma |[INS01](/pages/elicitacao/introspeccao#requisitos-persona-1) | US20, US21, US27, US28 |
| RF04 | O sistema deve possuir um chat acadêmico que possibilite a comunicação entre professor e aluno | [INS02](/pages/elicitacao/introspeccao#requisitos-persona-1) | US27, US28 |
| RF05 | O sistema deve possuir uma área para que os usuários possam deixar sugestões de melhoria para a plataforma | [INS03](/pages/elicitacao/introspeccao#requisitos-persona-1) | L2, US21, US25, US28 |
| RF06 | O sistema deve exibir os resultados obtidos nos aplicativos externos e integrados | [INS05](/pages/elicitacao/introspeccao#requisitos-persona-2) | L8, L5, US20, US25 |
| RF07 |  O sistema deve permitir a inserção de vídeo-aulas na plataforma | [INS06](/pages/elicitacao/introspeccao#requisitos-persona-2) | L4, US16, US17 |
| RF08 | O sistema deve permitir alteração de idioma para uso da plataforma | [INS07](/pages/elicitacao/introspeccao#requisitos-persona-3) | L7, L9, US15 |
| RF09 | Deve ser possível adicionar comentário em textos traduzidos de forma inadequada | [INS09](/pages/elicitacao/introspeccao#requisitos-persona-3) | L11, L17, L18, US21, US27 |
| RF10 | O sistema deve possuir uma lista de aplicativos de possível integração com a plataforma | [INS10](/pages/elicitacao/introspeccao#requisitos-persona-4) | US25 |
| RF11 | O sistema deve permitir a correção de contests por juri-online | [INS11](/pages/elicitacao/introspeccao#requisitos-persona-4) |  |
| RF12 | O sistema deve permitir o cadastro em grupo de alunos para realização de um contest | [INS12](/pages/elicitacao/introspeccao#requisitos-persona-4) | L6, L14, US19 <br> US26 | 
| RF13 | O sistema deve permitir que o usuário realize cadastro no sistema |[ST07](/pages/elicitacao/storytelling#requisitos-storytelling-3) |L1, L2, L3<br> US11, US12, US13 | 
| RF14 | O sistema deve permitir que o usuário altere informações de perfil | [ST08](/pages/elicitacao/storytelling#requisitos-storytelling-3)<br>[ST12](/pages/elicitacao/storytelling#requisitos-storytelling-4) |L1, L2, L3 <br> US14, US15 | 
| RF15 | O sistema deve permitir que o usuário mantenha disciplinas | [ST01](/pages/elicitacao/storytelling#requisitos-storytelling-1)<br>[ST09](/pages/elicitacao/storytelling#requisitos-storytelling-4) | L4, L5, L6<br> L9, L10, L11<br> US16, US24| 
| RF16 | O sistema deve permitir que o usuário crie uma seção TBL |[ST12](/pages/elicitacao/storytelling#requisitos-storytelling-4) |L6, L15, L16<br> US16, US24  | 
| RF17 | O sistema deve permitir que o usuário altere informações referentes às disciplinas criadas | [ST04](/pages/elicitacao/storytelling#requisitos-storytelling-2) | L7, L9, L10<br> L11, US15, US16 | 
| RF18 | O sistema deve permitir que o usuário consulte informações de alunos cadastrados em suas disciplinas | [INS01](/pages/elicitacao/introspeccao#requisitos-persona-1) | L12, L13, L14<br> L21, US17, US21<br>US25, US27, US28 |
| RF19 | O sistema deve permitir que o usuário crie testes para os alunos | [ST01](/pages/elicitacao/storytelling#requisitos-storytelling-1) | L17, L18, L19<br> L20, US26|
| RNF01 | O sistema deve ser capaz de suportar mais de 40 mil usuários logados | Pesquisa bibliográfica| - |
| RNF02 | Indicar com mais clareza o botão de criar exercícios | [ST05](/pages/elicitacao/storytelling#requisitos-storytelling-2) | L5, L6, L7,  | 
| RNF03 | O sistema deve indicar as restrições nos campo de informação no momento em que o usuário inserir os dados | [ST02](/pages/elicitacao/storytelling#requisitos-storytelling-1)<br>[ST10](/pages/elicitacao/storytelling#requisitos-storytelling-4) | L7, US13, US16 <br> US19, US22, US24, <br> US26 |
| RNF04 | O sistema deve permitir integração com aplicativos externos | [INS04](/pages/elicitacao/introspeccao#requisitos-persona-2) | L15, US20, US25, US26 | 

</div>

## Bibliografia

SAYÃO, M.; LEITE, J. **Rastreabilidade de requisitos**. Pontífica Universidade Católica do Rio de Janeiro. Tese de conclusão de curso, 2005.