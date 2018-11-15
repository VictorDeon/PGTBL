# Processo de medição GQM
***

![gqm](https://user-images.githubusercontent.com/14116020/45258263-06295c00-b38b-11e8-89ca-dec1a8373818.png)

O processo de medição deve ser estabelecido durante o projeto para assegurar que dados úteis e relevantes sejam coletados, e esse processo segue o padrão ISO/IEC/IEEE 15939:2008 que é o padrão internacional que define um processo de medição aplicável às disciplinas de gestão e engenharia de software e sistemas.

O processo utilizado será o GQM já que o GQM é uma abordagem mais específica, pois define questões para um objetivo específico e a partir das questões são definidas as métricas. A ideia base desta abordagem é, para cada meta estabelecida dentro da organização, identificar questões possíveis de serem respondidas com a análise de medidas coletadas para métricas, sendo a Medição então fundamentada em metas que a organização visa alcançar. O modelo de medida proposto por este método contém três níveis: **conceitual** (objetivos), **operacional** (questões) e **quantitativo** (métricas).

Um processo de medição de software direcionado aos objetivos produz medidas que proveem informações para importantes questões de negócio previamente identificadas. Uma vez que as medidas podem ser rastreadas de volta aos objetivos da organização, as atividades de coleta de dados não são executadas apenas pelo ato de coletar medidas, e sim com o propósito de que os dados coletados sejam analisados de forma a manter o foco nestes objetivos.

O GQM é composto das seguintes fases:

* **Planejamento**​: Envolve a seleção da aplicação a ser mensurada, e a definição, caracterização e planejamento do projeto;

* **Definição**​: Onde os objetivos, questões, métricas e hipóteses são definidas e documentadas;

* **Coleta de dados**​: Coletar os dados para atender as métricas definidas;

* **Interpretação​**: Na qual os dados coletados são analisados para identificar as respostas às questões e realizar o feedback a equipe.

***
## 1. Objetivos estratégicos
***

Foi definido dois objetivos estratégicos para a coleta de métricas:

<table>
  <tr>
    <td colspan="2"><b>O1: A qualidade de código</b></td>
  </tr>
  <tr>
    <td>Objeto</td>
    <td>Software TBL</td>
  </tr>
  <tr>
    <td>Propósito</td>
    <td>Melhorar</td>
  </tr>
  <tr>
    <td>Foco de qualidade</td>
    <td>Qualidade do código</td>
  </tr>
  <tr>
    <td>Ponto de vista</td>
    <td>Da equipe de desenvolvimento e gerência.</td>
  </tr>
  <tr>
    <td>Contexto</td>
    <td>Team Based Learning</td>
  </tr>
</table>

<table>
  <tr>
    <td colspan="2"><b>O2: O conhecimento da equipe.</b></td>
  </tr>
  <tr>
    <td>Objeto</td>
    <td>Equipe de desenvolvimento</td>
  </tr>
  <tr>
    <td>Propósito</td>
    <td>Melhorar</td>
  </tr>
  <tr>
    <td>Foco de qualidade</td>
    <td>Conhecimento da equipe em relação às tecnologias</td>
  </tr>
  <tr>
    <td>Ponto de vista</td>
    <td>Da equipe de desenvolvimento.</td>
  </tr>
  <tr>
    <td>Contexto</td>
    <td>Team Based Learning</td>
  </tr>
</table>


***
## 2. Questões
***

As questões são o foco de qualidade que deve ser respondido através das métricas coletadas para alcançar o objetivo estratégico proposto.

|Tópico|Descrição|
|------|---------|
|**Foco na qualidade**|São as questões focadas na qualidade|
|**Fontes de variação**|É o que pode variar no decorrer da coleta das métricas para responder às questões|
|**Hipótese de Baseline**|Como a equipe no momento responderia essas questões|
|**Impactos nas hipóteses de Baseline**|São os impactos que as fontes de variação causam nas hipóteses de baseline.|

### 2.1 Abstraction sheet da qualidade de código

#### 2.1.1 Foco na qualidade:

* Q1.1 O software está com uma cobertura de código aceitável?

* Q1.2 A qualidade do código está aceitável?

#### 2.1.2 Fontes de variação

* Complexidade de código

* Conhecimento da equipe em relação a tecnologia

#### 2.1.3 Hipótese de Baseline

* No momento não há cobertura de código

* O código está com uma qualidade aceitável

#### 2.1.4 Impactos nas hipóteses de Baseline

Caso a complexidade do código esteja fácil o esforço da equipe tende a diminuir, conseguindo ser mais produtivo e agregando mais qualidade e segurança ao cliente, além de diminuir o custo de manutenção, caso contrário, o esforço da equipe tende a aumentar, podendo ocasionar uma baixa qualidade na solução desenvolvida e a manutenção tende a ser muito cara.

Caso a equipe tenha dificuldade em aprender a tecnologia, ocasiona um atraso na entrega do produto e gera um produto com qualidade ruim e inseguro, consequentemente a insatisfação do cliente, porém se a equipe se adapta bem a tecnologia isso torna o desenvolvimento bem mais rápido e eficiente, gerando códigos com boa qualidade e seguros, consequentemente o usuário ficará satisfeito.

### 2.2 Abstraction sheet do conhecimento da equipe

#### 2.2.1 Foco na qualidade:

* Q2.1 A equipe está tendo conhecimento suficiente para desenvolver a aplicação?

#### 2.2.2 Fontes de variação

* Conhecimento da equipe em relação a tecnologia.

#### 2.2.3 Hipótese de Baseline

* No momento a equipe tem um conhecimento prévio da tecnologia.

* A tecnologia que causa mais dificuldade no momento são os testes em javascript, e o deploy contínuo.

#### 2.2.4 Impactos nas hipóteses de Baseline

* Caso a equipe tenha dificuldade em aprender a tecnologia, ocasiona um atraso na entrega do produto e gera um produto com qualidade ruim e inseguro, consequentemente a insatisfação do cliente, porém se a equipe se adapta bem a tecnologia isso torna o desenvolvimento bem mais rápido e eficiente, gerando códigos com boa qualidade e seguros, consequentemente o usuário ficará satisfeito.

***
## 3. Métricas de Qualidade
***

Durante a construção do escopo do plano de projeto, as métricas que são levantadas e dadas como candidatas, devem ser consideradas e analisadas no contexto em que vão ser coletadas, assim como é necessário verificar qual a validade e a importância da informação inserida no ambiente, para que os dados coletados sobres as entidades estabelecidas possam ser ratificadas e façam sentido completo, tanto para a equipe de medição quanto para os atores presentes no processo analisado. Deste modo, então, é possível, com os dados coletados, quantificar e/ou qualificar apropriadamente a fim de corroborar para os objetivos da organização. As métricas devem ser confiáveis, ou seja, devem produzir resultados coerentes com a realidade, sendo autônomo de condições externas de aplicação. Deve buscar, igualmente, ser prático, com a finalidade de manter um esforço de execução que vise a excelência, ser de fácil interpretação e de aplicação simples.

Será feito o uso de cinco métricas de qualidade de código e uma de conhecimento:

* Cobertura de Testes;

* índice de qualidade (Certification);

* Quantidade de issues geradas pela ferramenta de análise estática;

* Complexidade ciclomática;

* Quadro de conhecimento

O acompanhamento dos valores das métricas será realizado com auxílio das ferramentas discutidas em [Ferramentas Utilizadas](#ferramentas). As métricas são coletadas a partir da branch dev/master. A coleta é realizada após a finalização de cada funcionalidade e serão utilizadas para avaliar a necessidade de refatoração, conforme deliberado em cada métrica e possivelmente apontar vícios de programação, de forma que a equipe de gerência pode sugerir melhorias antes da codificação de novas funcionalidades e antes de disponibilizar o código na branch master.

### 3.1 Tipos de métricas

**Tipos de métricas**: Métrica é uma definição matemática, algorítmica ou função usada para obter uma avaliação quantitativa de um produto, processo ou recurso (ISO-9126-1, 1991).

|Tipo de métrica|Descrição|Exemplos|
|---------------|---------|--------|
|**Métrica Objetiva**|A medida relacionada independe do autor que a coleta|Normalmente são expressões numéricas ou representações gráficas de expressões numéricas que podem ser computadas de documentos de software|
|**Métrica Subjetivas**|Uma mesma métrica pode receber medidas diferentes para um mesmo alvo de coleta, instância de uma entidade, quando mensurada por autores distintos|Medidas relativas, baseada em estimativas pessoais ou de grupo (ex: bom, ruim, etc)|
|**Métrica Direta**|Caso a medida de uma métrica a ser coletada não depende da medida de outras métricas para compor o seu valor.|Por exemplo conhecimento da equipe|
|**Métrica Indireta**|Caso a medida de uma métrica a ser coletada depende da medida de outras métricas para compor o seu valor|Tamanho do software, depende da quantidade de linhas, arquivos e etc...|
|**Métrica Interna**|Aplicadas a um produto não-executável que permite avaliar os produtos de software antes do produto ser executável, também mede atributos internos de uma entidade ou indica atributos externos.|Especificações, código fonte, e etc...|
|**Métrica Externa**|Obtidas a partir do comportamento do sistema através de testes, operação ou observando sua execução em um ambiente e permite avaliar durante o teste e operação.|Número de bugs, erros, e etc...|

### 3.2 Tipos de escala

**Tipos de escala**: Definem proporções entre medidas de mesma unidade, variam em significado dos valores admitidos e operações sobre esses valores, pode ser ordinal, nominal, intervalo, racional ou absoluta

|Tipo de escala|Descrição|Exemplos|
|--------------|---------|--------|
|**Nominal**|Classes ou categorias para organizar as entidades, sem ordem definida|Cor dos olhos de pessoas, classes de defeitos, nomes de linguagens, classes de custos (custos diretos, custos indiretos), etc.|
|**Ordinal**|Classes ou categorias com noção de ordem entre elas. Números, se utilizados, significam apenas classificações e não é possível efetuar operações matemáticas com eles|Os níveis de maturidade do CMM (níveis de 1 a 5); Complexidade de uma função de um sistema (baixa, média, alta).|
|**Intervalo**|Preserva a importância da ordem dos resultados da escala ordinal, e ainda possui informações sobre o tamanho dos intervalos que separam seus pontos. Permite realizar adições e subtrações, mas não permite multiplicações e divisões. Possuem o “zero relativo”, o que não significa ausência do atributo|Temperatura; Intervalos de: datas, horários, etc.|
|**Racional**|Preserva a ordem, o tamanho dos intervalos entre entidades, mas apresenta também as razões entre elas. Incorpora o elemento zero absoluto (representando a total falta do atributo). Todas as funções aritméticas podem ser utilizadas aplicadas em cada intervalo do mapeamento, gerando resultados significativos|Tamanho, peso, altura, tempo entre falhas, valores de custos, prazos, esforços, etc.|
|**Absoluta**|Consiste em um tipo especial de escala racional, onde somente são admissíveis multiplicadores unitários, isto é, a medição é realizada por meio da contagem do número (quantidade) de elementos de uma determinada entidade. A grande diferença está no fato que a escala absoluta fixa a unidade de medida, não tem como ser representado por mais de uma unidade de medida|Número de defeitos encontrados no software, número de pessoas trabalhando em uma equipe, número de ocorrências de um determinado tipo etc.|

**Medidas**: Valores propriamente ditos

**Unidade**: Uma medida representa um valor de uma métrica em uma dada unidade.

### 3.3 Indicadores

Os indicadores são as bases as quais buscam auxiliar na interpretação e verificação das métricas definidas, pois os mesmo buscam, quando possível, representar numericamente os dados das métricas, ou representar de uma forma mais palpável para a compreensão, interpretação, análise, conclusão e agregação de outras métricas para a confecção de um relatório de resultados. Os indicadores estão apresentados incorporados às métricas.

***
## 4. Detalhamento das métricas
***

### 4.1 Cobertura de código

<table>
  <tr>
    <td colspan="2"><b>Questão 1.1: O software está com uma cobertura de código aceitável?</b></td>
  </tr>
  <tr>
    <td><b>Objetivo da medição</b></td>
    <td>Verificar a cobertura de código</td>
  </tr>
  <tr>
    <td><b>Entidade</b></td>
    <td>Produto</td>
  </tr>
  <tr>
    <td><b>Tipo</b></td>
    <td>Métrica objetiva, direta e externa</td>
  </tr>
  <tr>
    <td><b>Escala da Medição</b></td>
    <td>Racional</td>
  </tr>
  <tr>
    <td><b>Coleta</b></td>
    <td>
        <ul>
            <li><b>Responsável</b>: Equipe de Gerência</li>
            <li><b>Periodicidade ou Evento</b>​: por sprint</li>
            <li><b>Procedimentos​</b>: Será verificado utilizando uma ferramenta de cobertura de teste chamada codacy que rodará dentro do software, ela gera um tracking dos arquivos que necessitam de teste. Esse tracking demonstra uma porcentagem para cada arquivo, que indica a cobertura de testes deste.</li>
            <li><b>Armazenamento</b>: ​ Resultados da sprint - Wiki</li>
        </ul>
    </td>
  </tr>
  <tr>
    <td><b>Análise</b></td>
    <td>
        <ul>
            <li><b>Responsável</b>: Equipe de Gerência</li>
            <li><b>Valor aceitável</b>: Maior que 50% de cobertura de código, a medida a ser tomada caso não alcance é manter o nível de cobertura de código, e se possível aumentar o nível para que este alcance o nível ótimo.</li>
            <li><b>Valor ótimo</b>: Maior que 90% de cobertura de código, a medida a ser tomada caso não alcance é manter o nível de cobertura de código e tentar alcançar o 100%.</li>
            <li><b>Valor preocupante</b>: Menor que 50% de cobertura de código, a medida a ser tomada caso não alcance é priorizar cobertura de testes como um fator crítico na equipe, e focar todos os esforços possíveis a fim de aumentar o nível de cobertura</li>
        </ul>
    </td>
  </tr>
  <tr>
    <td><b>Indicadores</b></td>
    <td>O resultado desta métrica será dado em um valor de porcentagem que variará entre 0% e 100%, onde 0% significa que nenhum dos arquivos analisados pela ferramenta foi testado e 100% indica cobertura completa de testes.</td>
  </tr>
  <tr>
    <td><b>Qualidade de Produto de Software</b></td>
    <td>
        <ul>
            <li><b>Dimensão</b>: Segurança e Manutenibilidade na produção e evolução de software</li>
            <li><b>Característica</b>: Segurança</li>
            <li><b>Sub-característica</b>: Integridade - Verifique a integridade do sistema em relação ao código construído.</li>
            <li><b>Característica</b>​: Manutenibilidade</li>
            <li><b>Sub-característica</b>: Testabilidade - Verifica se os testes do código construído estão cobrindo as linhas de código necessárias.</li>
        </ul>
    </td>
  </tr>
</table>

### 4.2 Índice de certificação de projeto

<table>
  <tr>
    <td colspan="2"><b>Questão 1.2 A qualidade do código está aceitável?</b></td>
  </tr>
  <tr>
    <td><b>Objetivo da medição</b></td>
    <td>Verificar o índice de qualidade (Certificate Project)</td>
  </tr>
  <tr>
    <td><b>Entidade</b></td>
    <td>Produto</td>
  </tr>
  <tr>
    <td><b>Tipo</b></td>
    <td>Métrica objetiva, direta e interna</td>
  </tr>
  <tr>
    <td><b>Escala da Medição</b></td>
    <td>Ordinal</td>
  </tr>
  <tr>
    <td><b>Coleta</b></td>
    <td>
        <ul>
            <li><b>Responsável</b>: Equipe de Gerência</li>
            <li><b>Periodicidade ou Evento</b>: por sprint</li>
            <li><b>Procedimentos​</b>: Verificar o índice de qualidade disponibilizado pela ferramenta codacy que indicar a qualidade de código total de um repositório.</li>
            <li><b>Armazenamento</b>: ​ Resultados da sprint - Wiki</li>
        </ul>
    </td>
  </tr>
  <tr>
    <td><b>Análise</b></td>
    <td>
        <ul>
            <li><b>Responsável</b>: Equipe de Gerência</li>
            <li><b>Valor aceitável</b>: B e C, refatorar sempre que possível o código até atingir o valor ótimo.</li>
            <li><b>Valor ótimo</b>: A, manter a qualidade do código estável..</li>
            <li><b>Valor preocupante</b>: D e F, priorizar a refatoração do código com urgência, e focar todos os esforços possíveis a fim de aumentar o GPA.</li>
        </ul>
    </td>
  </tr>
  <tr>
    <td><b>Indicadores</b></td>
    <td>O resultado desta métrica será dado em um índice entre F e A, onde F significa que o código pode ir para o lixo, D significa que o código está ruim, C significa nota que o código está na média, B o código está bom e A o código está com uma qualidade excelente.</td>
  </tr>
  <tr>
    <td><b>Qualidade de Produto de Software</b></td>
    <td>
        <ul>
            <li><b>Dimensão</b>: Qualidade interna de código</li>
            <li><b>Característica</b>​: Manutenibilidade</li>
            <li><b>Sub-característica</b>: Modificabilidade - Verificar a modificabilidade medindo a qualidade interna de código.</li>
            <li><b>Característica</b>: Segurança</li>
            <li><b>Sub-característica</b>: Integridade - Verifique a integridade do sistema em relação a produção do software</li>
        </ul>
    </td>
  </tr>
</table>

### 4.3 Complexidade ciclomática e Churn

<table>
  <tr>
    <td colspan="2"><b>Questão 1.2 A qualidade do código está aceitável?</b></td>
  </tr>
  <tr>
    <td><b>Objetivo da medição</b></td>
    <td>Esta métrica diz respeito ao número de vezes que um arquivo foi alterado nos últimos 90 dias (Churn) e avalia a quantidade de caminhos de execução independentes a partir de um código fonte (Complexidade Ciclomática). Através delas a equipe de gerenciamento se encarrega de identificar pontos do projeto que estão demandando maior trabalho da equipe e tem uma grande complexidade utilizando como base os arquivos que mudam mais frequentemente avaliando quais são as suas qualidades relativas, em outras palavras, essas métricas fornece base técnica para avaliação empírica do direcionamento de esforços no projeto. Tal métrica é útil para avaliar fragilidades de especificações que podem estar gerando valores altos. Logo ela serve como base para a equipe decidir sobre refatorações em especificações, especialmente arquiteturais.</td>
  </tr>
  <tr>
    <td><b>Entidade</b></td>
    <td>Produto</td>
  </tr>
  <tr>
    <td><b>Tipo</b></td>
    <td>Métrica objetiva, direta e interna</td>
  </tr>
  <tr>
    <td><b>Escala da Medição</b></td>
    <td>Ordinal</td>
  </tr>
  <tr>
    <td><b>Coleta</b></td>
    <td>
        <ul>
            <li><b>Responsável</b>: Equipe de Gerência</li>
            <li><b>Periodicidade ou Evento</b>​: por sprint</li>
            <li><b>Procedimentos</b>: A ferramenta codacy gera um gráfico chamado Churn/Complexity onde terá vários pontos coloridos em diferentes posições do gráfico, o eixo X do gráfico é o CHURN e o eixo Y é a Complexidade dos arquivos, nesse gráfico que iremos coletar as informações. Na nova versão do Codacy a complexidade ciclomática do projeto vem em percentagem.</li>
            <li><b>Armazenamento</b>: ​ Resultados da sprint - Wiki</li>
        </ul>
    </td>
  </tr>
  <tr>
    <td><b>Análise</b></td>
    <td>
        <ul>
            <li><b>Responsável</b>: Equipe de Gerência</li>
            <li><b>Valor aceitável</b>: Complexidade entre 5% a 20% e arquivos com qualidade B a esquerda e abaixo do gráfico, refatorar sempre que possível o código do arquivo até atingir o valor ótimo.</li>
            <li><b>Valor ótimo</b>: Complexidade abaixo de 5% e arquivos com qualidade A a esquerda e abaixo do gráfico, manter a qualidade do código do arquivo estável.</li>
            <li><b>Valor preocupante</b>: Complexidade acima de 20% e arquivos com qualidade C, D e F a direita e acima do gráfico, priorizar a refatoração do código do arquivo com urgência, e focar todos os esforços possíveis a fim de aumentá-lo para o valor ótimo.</li>
        </ul>
    </td>
  </tr>
  <tr>
    <td><b>Indicadores</b></td>
    <td>O resultado desta métrica será dado um gráfico com pontos coloridos separados em posições distintas, os arquivos que tiverem mais a esquerda e abaixo no gráfico terá uma cor normalmente verde a amarela e indicadores A e B e estarão com complexidade entre 0% e 20%, é um valor de ótimo para aceitável, o os pontos/arquivos que tiverem a direita e acima do gráfico terá cores laranja para vermelho com indices de C, D e F que são valores preocupantes que necessitam ser observados, terão complexidades acima de 20%, consequentemente gera complexidade computacional custosa podendo refletir em tempo de espera em consultas. Pode ser útil para identificar churn alto, arquivos de baixa qualidade dentro de um repositório. O eixo X deste gráfico é o churn do arquivo, quanto mais a esquerda, é melhor. O eixo Y é a complexidade, quanto mais abaixo é melhor.</td>
  </tr>
  <tr>
    <td><b>Qualidade de Produto de Software</b></td>
    <td>
        <ul>
            <li><b>Dimensão</b>: Qualidade interna de código</li>
            <li><b>Característica</b>​: Manutenibilidade</li>
            <li><b>Sub-característica</b>: Modificabilidade - Verificar a modificabilidade medindo a qualidade interna de código.</li>
            <li><b>Característica</b>: Segurança</li>
            <li><b>Sub-característica</b>: Integridade - Verifique a integridade do sistema em relação a produção do software</li>
        </ul>
    </td>
  </tr>
</table>

### 4.4 Quantidade de issues

<table>
  <tr>
    <td colspan="2"><b>Questão 1.2 A qualidade do código está aceitável?</b></td>
  </tr>
  <tr>
    <td><b>Objetivo da medição</b></td>
    <td>Verificar a quantidade de issues geradas pela ferramenta de análise estática e identificar sua categoria e nível de gravidade</td>
  </tr>
  <tr>
    <td><b>Entidade</b></td>
    <td>Produto</td>
  </tr>
  <tr>
    <td><b>Tipo</b></td>
    <td>Métrica objetiva, direta e interna</td>
  </tr>
  <tr>
    <td><b>Escala da Medição</b></td>
    <td>Racional</td>
  </tr>
  <tr>
    <td><b>Coleta</b></td>
    <td>
        <ul>
            <li><b>Responsável</b>: Equipe de Gerência</li>
            <li><b>Periodicidade ou Evento</b>: por sprint</li>
            <li><b>Procedimentos</b>: Verificar a quantidade de issues por categoria geradas pela ferramenta de análise estática Codacy e o nível de gravidade de cada uma.</li>
            <li><b>Armazenamento</b>: ​ Resultados da sprint - Wiki</li>
        </ul>
    </td>
  </tr>
  <tr>
    <td><b>Análise</b></td>
    <td>
        <ul>
            <li><b>Responsável</b>: Equipe de Gerência</li>
            <li><b>Valor aceitável</b>: Menos de 50 issues, Refatorar sempre que possível o código até atingir o valor ótimo.</li>
            <li><b>Valor ótimo</b>: Nenhuma issue, Manter a qualidade do código estável.</li>
            <li><b>Valor preocupante</b>: Maior que 50 issues, Priorizar a refatoração do código com urgência utilizando de preferência folhas de estilo, e focar todos os esforços possíveis a fim de diminuir a quantidade de issues.</li>
        </ul>
    </td>
  </tr>
  <tr>
    <td><b>Indicadores</b></td>
    <td>O resultado desta métrica será dado em um valor que é a quantidade de issues que a ferramenta de análise estática de código encontrou, a ferramenta utiliza folhas de estilos normalmente adotadas para padronizar as linguagens, por exemplo a pep8 que é uma folha de estilo para a linguagem python padronizando seu código. Além disso cada issue é separado em categorias entre elas as mais importantes são Style, Error Prone, Unused code, security.</td>
  </tr>
  <tr>
    <td><b>Qualidade de Produto de Software</b></td>
    <td>
        <ul>
            <li><b>Dimensão</b>: Qualidade interna de código</li>
            <li><b>Característica</b>​: Manutenibilidade</li>
            <li><b>Sub-característica</b>: Modificabilidade - Verificar a modificabilidade medindo a qualidade interna de código.</li>
            <li><b>Característica</b>​: Segurança</li>
            <li><b>Sub-característica</b>: Integridade - Verifique a integridade do sistema em relação a produção do software</li>
        </ul>
    </td>
  </tr>
</table>

### 4.5 Quadro de conhecimento

<table>
  <tr>
    <td colspan="2"><b>Questão 2.1 A equipe está tendo conhecimento suficiente para desenvolver a aplicação?</b></td>
  </tr>
  <tr>
    <td><b>Objetivo da medição</b></td>
    <td>Verificar o quadro de conhecimento e ver quais tecnologias precisa ser estudada com mais intensidade pela equipe de desenvolvimento, fazendo dojos, e tutoriais.</td>
  </tr>
  <tr>
    <td><b>Entidade</b></td>
    <td>Produto</td>
  </tr>
  <tr>
    <td><b>Tipo</b></td>
    <td>Métrica subjetiva, direta e externa</td>
  </tr>
  <tr>
    <td><b>Escala da Medição</b></td>
    <td>Nominal</td>
  </tr>
  <tr>
    <td><b>Coleta</b></td>
    <td>
        <ul>
            <li><b>Responsável</b>: Equipe de Gerência</li>
            <li><b>Periodicidade ou Evento</b>​: por sprint</li>
            <li><b>Procedimentos</b>: Verificar como está o quadro de conhecimento a cada sprint e identificar as tecnologias que os desenvolvedores estão tendo mais dificuldade de aprender.</li>
            <li><b>Armazenamento</b>: ​ Resultados da sprint - Wiki</li>
        </ul>
    </td>
  </tr>
  <tr>
    <td><b>Análise</b></td>
    <td>
        <ul>
            <li><b>Responsável</b>: Equipe de Gerência</li>
            <li><b>Valor aceitável</b>: :neutral_face:, Estudar a tecnologia sempre que houver tempo.</li>
            <li><b>Valor ótimo</b>: :sunglasses: e :relieved:, Tem domínio sobre a tecnologia.</li>
            <li><b>Valor preocupante</b>: :confused: e :worried:, Criar dojos e estudar a tecnologia mais a fundo com a equipe.</li>
            <li><b>Desistência</b>: :trollface:, Encontrar outra tecnologia para substituí-la na função que ela ia desempenhar.</li>
        </ul>
    </td>
  </tr>
  <tr>
    <td><b>Indicadores</b></td>
    <td>O resultado desta métrica será dado no quadro de conhecimento, na qual o eixo x será as tecnologias empregadas no projeto e o eixo y será o nome dos integrantes da equipe, teŕa seis rostos que dirá se o integrante tem domínio da tecnologia (:sunglasses: e :relieved:), está aprendendo e consegue se virar sozinho (:neutral_face:), está tendo dificuldades na tecnologia (:confused: e :worried:) ou se desistiu da tecnologia (:trollface:)</td>
  </tr>
</table>

***
## 5. Rastreabilidade
***

Junto com o processo de GQM que foi o paradigma que norteou a equipe durante as fases de concepção e planejamento do projeto, a rastreabilidade seguiu com a visão, onde a definição do plano seguiu no formato ​ top-down ​ de objetivos, questões e métricas, então foi elaborado uma matriz de rastreabilidade que auxiliará a interpretação dos dados coletados, este que se dá na forma de ​ bottom-up ​ para melhor percepção dos resultados gerados pela medição. No topo da matriz estão os objetivos, abaixo são mostradas as questões e na sua base são apresentadas as métricas abstraídas. Lembrando que cada métrica está conectada a questão que deu origem a ela, e as matrizes estão organizadas por objetivo.

![rastreabilidade](https://user-images.githubusercontent.com/14116020/27944268-2f4f06f0-62bc-11e7-9652-8edb1ba800a9.png)

<table>
  <tr>
    <th>Objetivos</th>
    <th>Questões</th>
    <th>Métricas</th>
  </tr>
  <tr>
    <td rowspan="4">O1: A qualidade de código</td>
    <td>Q1.1 O software está com uma cobertura de código aceitável?</td>
    <td>M1.1.1 Cobertura de Testes</td>
  </tr>
  <tr>
    <td rowspan="3">Q1.2 A qualidade do código está aceitável?</td>
    <td>M1.2.1 índice de qualidade (Certification)</td>
  </tr>
  <tr>
    <td>M1.2.2 Quantidade de issues geradas pela ferramenta de análise estática</td>
  </tr>
  <tr>    
    <td>M1.2.3 Complexidade ciclomática e Churn</td>
  </tr>
  <tr>
    <td>O2: O conhecimento da equipe.</td>
    <td>Q2.1 A equipe está tendo conhecimento suficiente para desenvolver a aplicação?</td>
    <td>M2.1.1 Quadro de conhecimento</td>
  </tr>
</table>

***
## 6. Critérios de Qualidade
***

### 6.1 Qualidade de código

O [PEP8 - Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/) estabelece padrões de codificação que devem ser utilizados na implementação do software. A partir do PEP8 foi desenvolvido a Folha de estilo que visa aplicar uniformidade na escrita de código buscando melhorar a qualidade do mesmo em termos de legibilidade e manutenibilidade. Nela constam parâmetros tais como espaçamentos, linhas em branco, nomes de funções, variáveis e afins, e pequenas técnicas simplistas que visam impactar em um código mais eficaz através da identificação de anti-patterns, a ferramenta Codacy utiliza do pylint para padronizar a folha de estilo no código.

### 6.2 Integração Contínua

É uma prática de integração frequente das diversas partes de código de forma a evitar precocemente diversos problemas que possam surgir em uma integração de código tardia. O desenvolvimento do projeto contará com auxílio da ferramenta Travis CI para integração contínua de código.

O Travis apresenta um dashboard com todas as builds feitas. As builds são feitas toda vez que há um novo commit no repositório do projeto na branch dev, o Travis irá travar qualquer pull request que não passe na build, testes e que esteja com a qualidade de código ruim.

### 6.3 Usabilidade

O framework Bootstrap será utilizado visando melhorar a experiência de usuário e implementar responsividade nas telas do sistema. Serão feitos protótipos de alta fidelidade e validados com o cliente antes da construção da interface, para que as mesmas sigam o protótipo aprovado pelo cliente sendo ele reutilizável.

Utilizar de algumas ferramentas de UX para que o software possa ter uma boa aceitação no meio social, técnicas com 360 view entre outras...

***
## 7. Ferramentas Utilizadas
***

* [Travis CI](https://travis-ci.org/) - Integração contínua.

* [pylint](https://www.pylint.org/) - Adequação a folha de estilo; Análise estática; Prevenção de impacto em Complexidade Ciclomática.

* [Codacy](https://www.codacy.com/app/VictorArnaud/TBL-Service/dashboard) - Avaliação das métricas de qualidade de código e cobertura de testes.

* [Bootstrap](http://getbootstrap.com/) - Framework para implementação de interface de usuário responsiva e melhoria da experiência de usuário como um todo.

* [HTML/CSS](https://www.w3schools.com/) - Ferramenta para criação do protótipos de alta fidelidade que será usado no sistema também.

* [Vagrant](https://www.vagrantup.com/docs/) - Ferramenta para simular o ambiente de produção.

* [Docker](https://docs.docker.com/) - Ferramenta para gerar o container de produção do projeto.

***
## 8. Monitoramento e Controle da Qualidade
***

**Documentação**: A equipe de gerência de projeto deverão realizar uma leitura minuciosa dos planos de gerenciamento após tais serem elaborados, de forma a elucidar eventuais falhas ou melhorias aplicáveis.

**Métricas**: Ao final de cada iteração da fases de construção e transição realizar a coleta das métricas estabelecidas e avaliar se os padrões de qualidade estão sendo atendidos. Caso não estejam, a equipe deverá tentar alocar tempo para refatoração do código de acordo com os indicadores das métricas, essas métricas serão apresentadas a equipe de desenvolvimento sempre nas retrospectiva da sprint.

**Usabilidade**: Os desenvolvedores deverão se ater previamente a responsividade das telas, conforme requisito não funcional de usabilidade especificado. Ao final de cada iteração serão realizadas rotinas de verificação de responsividade das telas e facilidade de uso.
