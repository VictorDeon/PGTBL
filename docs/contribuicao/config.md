# Contribuindo com o PGTBL.
***

Caso queira contribuir com o projeto, talvez seja uma boa ideia começar pelo [README](https://github.com/VictorArnaud/TBL/blob/master/README.md) para conhecer melhor sobre nós. 

Outro documento importante e que deve ser lido é o [Código de Conduta](https://github.com/VictorArnaud/TBL/blob/master/.github/CODE_OF_CONDUCT.md).

Obrigado por contribuir! Sua ajuda será recebida com muita gratidão!

***
## 1. Como eu posso contribuir?
***

### 1.1 Reportando um Bug

Esse projeto segue um padrão de _Issues_. Logo, caso encontre um bug, verifique se ele não se encontra em uma das nossas _Issues_. Os bugs devem ser marcados com _tag (label)_ __bug__.

Se o bug encontrado não consta nas _Isses_, basta abrir uma [Nova _Issue_](https://github.com/VictorArnaud/TBL/issues/new).

### 1.2 Adicionando e/ou modificando alguma funcionalidade

Primeiro verifique que não existe nenhuma [_Issue_](https://github.com/VictorArnaud/TBL/issues) a respeito dessa modificação e/ou adição.

Caso não exista, crie uma [Nova _Issue_](https://github.com/VictorArnaud/TBL/issues/new). Dê um título significativo a ela, coloque uma descrição e pelo menos uma _label_.

As mudanças devem ser submetidas através de _Pull Requests_.

***
# 2. Padrão de _Commit_
***

### 2.1 Por questões de padronização recomendamos que sigam nosso estilo de _commit_:

Os _commits_ devem ser todos em __inglês__;

Ele deve conter um título curto e objetivo do que foi feito naquele _commit_;

Se for preciso, após esse título, deve-se descrever, com um pouco mais de detalhes, todas as atividades executadas.

Caso esteja trabalhando em com algum associado assine nos seus _commits_ os seus parceiros

__Exemplo:__

```
  Creating project community files (Título curto e objetivo)

  Issue #01

  Adds project license (Descrição de uma das atividades)

  Adds project code of conduct file

  Adds project contributing file

  Adds project issue template file

  Adds projects pull request file

  Signed-off-by: Victor Arnaud <victorhad@gmail.com> (Assinatura de parceria)
```

***
## 3. Política de _Branchs_
***

![Política de branchs](https://cloud.githubusercontent.com/assets/14116020/21487025/bcc38f2c-cba6-11e6-9447-f392a31a2b2d.png)

A política de branches que será utilizada no decorrer do projeto seguirá o modelo descrito na imagem acima: para cada funcionalidade a ser implementada será criada uma branch a partir da branch devel, que estará em constante atualização com a branch master e vice versa.

Assim que cada funcionalidade for completada, será aberto um pull request (feito pela equipe de desenvolvimento) da branch correspondente à funcionalidade para a branch devel, para que esta seja aprovada.

O servidor de integração contínua estará funcionando em cima da branch master e devel. Ao fim de cada sprint, será realizado um rebase da branch devel para a branch master e então será realizado o processo de integração contínua do projeto. Tanto a branch master como a devel estarão em constante atualização, para que as próximas funcionalidades a serem implementadas tenham sempre o projeto mais atualizado possível.

Essa Política de Branches deverá guiar os desenvolvedores na forma de organização de suas contribuições ao repositório.

__master__ - Branch principal do repositório onde será permitida somente a integração de software consolidado e testado. Essa branch será exclusiva para a entrega de Realeases, ou seja, um conjunto maior de funcionalidades que integram o software, aqui estará a versão _**stable**_ do software.

__dev__ - Branch para integração de novas funcionalidades, onde será permitido a entrega das features desenvolvidas e que estão em um estágio avançado de completude. Será o branch base para o início do desenvolvimento das features e da correção de bugs. Aqui também serão _mergeadas_ as releases.

__nome-da-feature__ - Branch utilizada para o desenvolvimento de novas features do _backlog_. Caso a feature tenha sida proposta por uma _issue_ do repositório e aceita no _backlog_ o nome deverá conter o número da _issue_. 
Ex: US01_<nome-da-nova-feature> (Considerando que a feature tenha sido solicitada na _issue_ #1)

***
## 4. Política de _Pull Request_
***

Para que o "Pull Request" das funcionalidades seja devidamente aceito, esta deve estar devidamente testada e conforme os padrões de commit e estilo de código. Além disso, a build da Integração Contínua deve estar "passando" para tal funcionalidade e o pull request deve ser aberto seguindo o padrão estipulado no template.

***
## 5. Política de Versionamento
***

Todos os artefatos de gerenciamento devem informar sua versão atual no seguinte formato: **X.Y.Z**, descrito abaixo:

**X**: Apenas incrementa quando há mudanças que quebram a estrutura do projeto ou que disponibiliza uma versão estável para uso do projeto.

* **X < 1**: A versão do projeto não é estável.

* **X >= 1**: A versão do projeto é estável.

**Y**: Apenas incrementa quando é realizada a alteração ou adição de alguma nova funcionalidade.

**Z**: Apenas incrementa quando são realizadas correções ou alterações no código.
