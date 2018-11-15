# DevOps
***

De acordo com a Amazon DevOps é a combinação de filosofias, práticas e ferramentas que aumentam a capacidade de distribuir aplicativos e serviços em alta velocidade. Essas velocidade permite que seus clientes sejam atendidos de forma melhor e as empresas conseguem competir de forma mais eficaz no mercado. Com esse novo modelo, as equipes de desenvolvimento e operações não são mais separadas, ou seja, os engenheiros trabalham durante todo o ciclo de vida do aplicativo, da fase de desenvolvimento e testes à fase de implantação e operações.

Essas equipes usam práticas para automatizar processos que sempre foram feitas de maneira manual e lenta. Eles usam várias técnologias que o auxiliam a automatizar todo esse processo que envolve a infraestrutura do software e isso aumenta ainda mais a velocidade e produtividade da equipe.

A Amazon cita alguns benefícios do DevOps, são eles: velocidade, en- trega rápida, confiabilidade, operações em escala, colaboração melhorada e segurança.  Além disso o modelo de DevOps é importante já que o software já não apenas sustenta uma atividade empresarial, ele tornou-se um componente integral de cada parte de uma empresa. O objetivo principal desse modelo é remover as barreiras entre duas equipes tradicionalmente separadas, desenvolvimento e operações, com essa abordagem as duas equipes trabalham juntas para otimizar a produtividade dos desenvolvedores e a confia- bilidade das operações de forma a automatizar alguns processos que antes eram feitos de forma manual e que gerava uma certa dependencia entre as equipes.

De acordo com Amazon existem algumas práticas essenciais que ajudam as empresas a inovar mais rapidamente por meio da automação e da simplificação dos processos de desenvolvimento de software e gerenciamento de infraestrutura. A maioria dessas práticas já são realizadas e mencionadas em algumas metodologias como o XP. São elas: integração contínua, entrega contínua, microsserviços, infraestrutura como código, monitoramento e registro em log, comunicação e colaboração.

***
### Processo de DevOps
***

![devops](https://user-images.githubusercontent.com/14116020/45258237-c2365700-b38a-11e8-96fb-3ca11baa5a45.png)

#### Criação da branch para fazer a funcionalidade:

* **Descrição**: O desenvolvedor irá criar uma nova branch a partir da devel para criar a nova funcionalidade proposta de acordo com a política de branch estabelecida.
* **Entradas**: N/A
* **Saídas**: Nova branch da funcionalidade.

#### Construção do código:

* **Descrição**: Com a nova branch criada o desenvolvedor irá criar o código para a nova funcionalidade.
* **Entradas**: Branch
* **Saídas**: Nova funcionalidade.

#### Envio do código para o github:

* **Descrição**: Assim que o código estiver pronto, o desenvolvedor irá enviar o código para o repositorio do github.
* **Entradas**: Nova funcionalidade
* **Saídas**: N/A

#### Pull Request da branch atual para a branch devel:

* **Descrição**: Assim que o código for enviado para o github o desenvolvedor irá abrir um Pull Request para que comece o processo de Integração Contínua e Deploy Continúo.
* **Entradas**: Nova funcionalidade
* **Saídas**: N/A

#### Execução do Travis CI:

* **Descrição**: Processo automatizado para execução da Integração Contínua e Deploy Contínuo.
* **Entradas**: Nova funcionalidade
* **Saídas**: N/A

#### Testes e Qualidade de Código:

* **Descrição**: Na integração Contínua de forma automatizada será executado os testes unitários, integração e aceitação, além de verificar a qualidade do código por meio da ferramenta de análise estática.
* **Entradas**: Nova funcionalidade
* **Saídas**: Relatório com a cobertura de teste e qualidade de código.

#### Aprovação e Merge do Pull Request:

* **Descrição**: Assim que a integração contínua for finalizada será feito o merge do código para a branch devel ou master e começará o deploy contínuo do software.
* **Entradas**: Nova funcionalidade
* **Saídas**: Versão publicavel do software.

#### Publicação das imagens no Dockerhub:

* **Descrição**: Por meio de Scripts automatizados o deploy continuo irá mandar a imagem do docker de homologação ou produção gerada para o respositório de imagens chamado Dockerhub.
* **Entradas**: Imagem do software.
* **Saídas**: Versão publicavel da imagem do software de homologação ou produção.

#### Conexão na máquina de deploy:

* **Descrição**: Por meio de SSH o script irá entrar na máquina de homologação ou produção
* **Entradas**: Scrips de conexão.
* **Saídas**: Conexão na máquina de homologação ou produção.

#### Atualização dos ambientes com a última versão dos containers:

* **Descrição**: Assim que tiver dentro da máquina o script irá atualizar o respo- sitório com as novas modificações e irá subir o software por meio das imagens armazenadas no dockerhub.
* Entradas**: Scrips de conexão e Imagens do Dockerhub.
* Saídas**: Software em produção ou Homologação.

#### Disponibilidade da nova versão para o usuãrio:

* **Descrição**: Assim que subir a imagem a nova versão do software estará pronta para uso.
* **Entradas**: Scrips de conexão e Imagens do Dockerhub.
* **Saídas**: Software em produção ou Homologação.

#### Pull Request da branch devel para a branch master:

* **Descrição**: Se o processo acima foi dentro da branch devel, ou seja, ambiente de homologação, o desenvolvedor terá que mandar um Pull Request para a branch master para subir o ambiente de produção.
* **Entradas**: Novas Funcionalidade.
* **Saídas**: Software em produção.
