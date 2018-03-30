# Plano Verificação e Validação
***
## 1. Verificação
***

O propósito do processo Verificação é confirmar que cada serviço e/ou produto de trabalho do processo ou do projeto atende apropriadamente os requisitos especificados [Pressman, 1995].

### 1.2 Processo de verificação

![Processo de Verificação](https://i.imgur.com/DZPPxCY.png)

O processo é detalhado pelo guia, segundo o SOFTEX(2011), em 6 tarefas gerais:

* **VER 1**: Identificar os produtos de trabalho a serem verificados.
* **VER 2**: Desenvolver e implementar uma estratégia de verificação, com definição de um cronograma, revisores envolvidos, métodos para verificação e qualquer material a ser utilizado na verificação.
* **VER 3**: Identificar critérios e procedimentos para verificação dos produtos de trabalho, além da definição do ambiente de verificação.
* **VER 4**: Executar revisão por pares e testes e atividades de verificação.
* **VER 5**: Identificar e registrar defeitos.
* **VER 6**: Analisar os resultados gerados e encaminhar aos envolvidos.

## 2. Validação

O objetivo da validação é validar que um produto de software atenderá a seu objetivo quando colocado no ambiente para o qual foi desenvolvido [Sommerville, 2007].

De forma geral o processo de validação tem seu foco em como avaliar a qualidade de um produto ou componente de produto, assegurando que os objetivos e ou necessidades dos clientes sejam atendidas quando colocado em seu ambiente de produção, ou seja, o objetivo da validação é garantir que o produto correto está sendo desenvolvido [SOFTEX, 2011].

### 2.2 Processo de validação

![Processo de Validação](https://i.imgur.com/ZL1YiAr.png)

O processo é detalhado pelo guia, segundo o SOFTEX(2011), em 7 tarefas gerais, como resultados esperados:

* **VAL 1**: Identificar os produtos de trabalho a serem validados.
* **VAL 2**: Desenvolver e implementar uma estratégia de validação, com definição de um cronograma, revisores envolvidos, métodos para validação e qualquer material a ser utilizado na validação.
* **VAL 3**: Identificar critérios e procedimentos para validação dos produtos de trabalho, além da definição do ambiente de validação.
* **VAL 4**: Executar atividades de validação para garantir que o produto esteja pronto para ser disponibilizado em ambiente de uso.
* **VAL 5**: Identificar e registrar problemas.
* **VAL 6**: Analisar os resultados obtidos e encaminhar aos envolvidos.
* **VAL 7**: Obter evidências  de  que  os  produtos  de  software  desenvolvidos  estão prontos para o uso pretendido são fornecidas.

***
## 3. Técnicas estáticas
***

São métodos usados para garantir a qualidade do software que não necessita de uma versão executável do programa. Por este motivo podem ser utilizadas em todas as fases do desenvolvimento do software, pode verificar tanto o produto quanto o processo de software.

As técnicas estáticas são utilizadas para Verificação de software, pois revelam se há correspondência entre o produto final e suas especificações, mas não são úteis para avaliar um software operacionalmente.

### 3.1 Principais métodos de Revisão Técnica 

#### 3.1.1 Inspeção

A inspeção é um processo de revisão formal de software e corresponde a uma das mais  importantes atividades de Garantia de Qualidade de Software, sendo que o principal objetivo é descoberta antecipada de falhas, ou seja, produção de uma saída incorreta em relação à especificação, de modo que elas não se propaguem para o passo seguinte do processo de software.

A inspeção visa encontrar erros lendo, entendendo o que o documento descreve e checando através de um checklist as propriedades de qualidade requeridas. É composta por seis fases, que são: 

1. Planejamento; 
2. Apresentação; 
3. Preparação; 
4. Reunião de Inspeção;
5. Retrabalho e 
6. Acompanhamento

#### 3.1.2 Walkthrough

Nesta técnica a revisão é feita através de uma execução passo a passo de um procedimento ou programa, porém realizada no papel. O objetivo é encontrar erros. Dura em média uma a duas horas.

Envolve equipes pequenas de três a cinco pessoas, onde é feita uma simulação da execução por cada revisor, controlada um testador que durante a reunião disponibiliza um conjunto de casos de teste e monitora os resultados obtidos de cada revisor.

#### 3.1.3 Peer-Review

É uma técnica formal de inspeção de código realizada em pares de programadores com mesmo nível de conhecimento. O objetivo desta técnica é obter pontos de vista diferentes do desenvolvedor e revisar o material, a fim de encontrar problemas de qualidade.

Apenas um programa ou algumas funcionalidades/documentos são revisados de cada vez. Os resultados obtidos vão para um relatório para a revisão e se forem pertinentes passam para o relatório final oficial. Deve ser analisado o produto não o desenvolvedor.

***
## 4. Técnicas dinâmicas (plano de teste)
***

### 4.1 Introdução

Testes têm como objetivo verificar dinamicamente o comportamento de um programa, usando um conjunto de casos de teste adequadamente selecionados, em relação ao seu comportamento esperado [IEEE, 2004].

Este documento tem como objetivo dar a base para a criação dos casos de teste, definindo conceitos e estabelecendo ferramentas para a criação e execução dos casos de teste. Entre os conceitos temos: níveis de testes, tipos de testes, os recursos necessários e o ambiente.

### 4.2 Níveis de teste

Definem o momento do ciclo de vida do software em que são realizados testes.

**Teste de unidade**: Cada unidade do programa é testada, isolada das demais unidades. Esse teste, conhecido como teste de unidade, verifica se a unidade funciona de forma adequada aos tipos de entrada esperados. Normalmente na orientação a objeto são as classes ou modelos. Ele a testa de maneira isolada geralmente simulando as prováveis dependências que aquela unidade tem. (Myers et al. 2004)

**Teste de Integração**: Quando todas as unidades já tiverem sido testadas, a próxima fase é realizar o teste de integração, para assegurar que as interfaces entre as unidades foram definidas e tratadas adequadamente. É aquele que testa a integração entre duas partes do seu sistema. Os testes das controladora, por exemplo, onde seu teste vai até o banco de dados, é um teste de integração. Afinal, você está testando a integração do seu sistema com o sistema externo, que é o banco de dados. Testes que garantem que suas classes comunicam-se bem com serviços web, escrevem arquivos texto, ou mesmo mandam mensagens via socket são considerados testes de integração. (Myers et al. 2004)

**Teste de Sistema**: Funcionamento do sistema como um todo, com todas as unidades trabalhando juntas. De acordo com o MPS.BR o teste do sistema envolve: teste funcional (verifica se o sistema integrado realiza as funções especificadas nos requisitos); teste de desempenho (avalia como o sistema se comporta em relação aos requisitos não-funcionais especificados, tais como tempo de resposta, uso do processador, segurança, dentre outros); teste de aceitação (Verificar a iteração de um usuário com o software, documentação do usuário, treinamento e etc); e teste de instalação (São testes de scripts de instalação para verificar se o software é instalado sem nenhum problema no host dos clientes). (Myers et al. 2004)

### 4.3 Tipos de testes

Segue abaixo os tipos de testes a serem aplicados ao projeto.

* **Funcional**: Teste baseado em requisitos funcionais, ou seja, funcionalidades do software.

* **Não funcional**: Teste baseado em requisitos não funcionais, no caso, qualidade de código.

Ambos os testes serão automatizados utilizando as ferramentas descritas na [sessão 4.4.2](#automatizado)

### 4.4 Recursos necessários e Técnicas

Técnica é o processo que vai assegurar perfeito funcionamento de alguns aspectos de software ou de sua unidade.

#### 4.4.1 Técnicas

**Caixa preta**: Aborda o software de um ponto de vista macroscópico e estabelece os requisitos de teste a partir da especificação do produto. Esse teste é baseado na analise funcional do software ele garante que os requisitos funcionem conforme o especificado, ele não se preocupa na forma como ele foi implementado, é inseridos alguns dados e espera-se na saída o resultado de como foi projetado os requisitos. Tal tipo de teste é indicado para detectar erros de interface, de comportamento e/ou desempenho, podendo ser aplicada em todas as fases de testes (unidade, integração, sistema e aceitação). Esta técnica também é chamada de “comportamental” ou “funcional”; (Myers et al. 2004)

**Caixa branca**: Estabelece os requisitos de teste com base na implementação do código. Esse teste tem por objetivo testar o código fonte e elaborando casos de teste que cubram as funcionalidades do componente de software, ele testa cada linha de código possível, testar os fluxos básicos e os alternativos. Esta técnica também é chamada de “caixa-de-vidro” ou “estrutural”; (Myers et al. 2004)

**Particionamento de equivalência**: É uma técnica que agrupa e otimiza casos de testes, afim de fazer a maior cobertura possível do sistema, é uma técnica caixa preta. Ela propõe a separação das possíveis entradas em categorias diferentes. O objetivo dessa técnica é eliminar os casos de testes redundante, por exemplo, valores entre 1990 e 2000, podemos pegar um único representante para todos esses casos, 1993 por exemplo e pegamos representantes para dados invalidos, como dados negativos ou fora do intervalor proposto, por exemplo, -10, 1980, 2001 e etc... Os casos de teste devem ser construídos a partir das partições criadas. (Myers et al. 2004)

**Análise de valor limite**: Também é uma técnica caixa preta que visa identificar o comportamento nos limites de uma partição de equivalência, ou seja, seus máximus e mínimus, que é onde existe maior probabilidade de estar incorreto. Os limites são áreas onde testes estão mais propensos a indicar defeitos. Análise do valor limite pode ser aplicada em todos os níveis de teste. Por exemplo, os valores limites de 1900 a 2004 são 1899, 1900, 2004, 2005. Ela complementa o particionamento de equivalência. (Myers et al. 2004)

#### 4.4.2 Ferramentas

|Ferramenta|Definição|Aplicação|
|----------|---------|---------|
|Pytest do django|pytest é uma ferramenta de teste de Python com todas as características que ajuda a escrever melhores programas|Testes funcionais unitários|
|Codacy|Ferramenta de revisão de código e monitoramento de qualidade de código |Análise estática|

### 4.5 Ambiente de teste

É uma organização específica de configurações de hardware, software e ambiente associadas necessárias à condução de testes precisos que permitam a avaliação dos Itens de Teste-alvo.

**Ambiente de desenvolvimento**: É o ambiente que os desenvolvedores utilizam para construir o software, pode ser a sua máquina ou uma máquina virtual que você utilize para programar, normalmente executam teste unitários e de integração.

**Ambiente de teste**: Normalmente utilizado para testar novas versões do produto, é uma infra-estrutura de testes integrados na qual versões estáveis dos componentes ou rotinas comuns em desenvolvimento ou não são instaladas e testadas. Por exemplo, ao atualizar um componente é necessário ter uma ideia do impacto desta alteração nos produtos dela dependentes.

**Ambiente de homologação**: Ambiente de homologação: É uma replica do ambiente de produção, seu objetivo é oferecer aos futuros usuários do sistema a possibilidade de testar as funcionalidades dos novos produtos de desenvolvimento e encontrar possíveis incorreções de resultados ou comportamentos, usado para testes de performance, estresse e de aceitação, entre outros. Devem esta sob a gestão da equipe de gestão e suporte, os desenvolvedores não devem possuis acesso privilegiado a esse ambiente, isso permite com que os desenvolvedores possar ter a mesma experiência dos usuários finais.

**Ambiente de produção**: É onde os usuários finais acessarão o software, normalmente é um host na nuvem, como a AWS, Digital Ocean entre outros.

|Nível de teste|Volume de dados|Origem dos dados|Ambiente|
|--------------|---------------|----------------|--------|
|Teste Unitário|Volume pequeno|Criação manual|Ambiente de desenvolvimento|
|Teste de Integração|Volume pequeno|Criação manual|Ambiente de desenvolvimento e Ambiente de teste|
|Teste de Sistema|Volume grande|Criação automatica, dados reais|Ambiente de teste|
|Teste de Aceitação|Volume grande|Criação manual, dados reais|Ambiente de homologação|

Os testes deverão ser feitos utilizando máquinas virtuais para simular os ambientes.

### 4.6 Produtos gerados

* **Relatório**: Relatório técnico das revisões dentro de cada sprint.
* **Teste automatizados**: Teste automatizados utilizando código como documentação.

***
## Referências
***

* Codacy. Disponível em: https://www.codacy.com/. Acesso em: 15 de Outubro de 2017
* IEEE 2004;
* MELO, Silvana  M. . Inspeção de software. Instituto de Computação e Matemática Computacional – Universidade de São Paulo, São Carlos;
* MYERS, Glendford J. .The Art Of Software Testing. 2ª Edição 2004;
* SOMMERVILLE, Ian. Engenharia de Software - 8ª Edição 2007;
* PRESSMAN, Roger s. Engenharia de Software – 1995;
* Pytest. Disponível em: https://docs.pytest.org/en/latest/#. Acesso em: 15 de Outubro de 2017
* SOFTEX. Guia de Implementação – Parte 9: Implementação do MR-MPS - 2011;
