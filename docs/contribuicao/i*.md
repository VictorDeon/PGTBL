## Definição

O framework de modelagem i* (i-estrela), originalmente proposto por Yu, trata da modelagem de contextos organizacionais tomando como base os relacionamentos de dependência entre os atores participantes.
 
O principal objetivo no i* é representar, através de modelos, os atores participantes e as dependências entre os mesmos, para que suas metas próprias sejam alcançadas, recursos sejam fornecidos, tarefas sejam realizadas e metas flexíveis sejam “razoavelmente satisfeitas”.
 
Podemos ler suas dependências da seguinte forma: Ator1 depende do ator2 para atingir uma meta, ou fornecer um recurso ou realizar uma tarefa, e etc...
 
De acordo com a legenda os atores são divididos em 3 que são os agentes, posições e papéis, no caso um agente ocupa uma posição e realiza um papel, tendo como relação de dependência as metas, tarefas, recursos e _softgoals_

_Softgoals_ são os requisitos não funcionais definido no [Framework NFR](nfr)
 
## Modelo SD (modelo de dependências estratégicas)
 
O modelo SD exibe os relacionamentos de dependência estratégica entre os atores da organização, utilizando para isso uma rede de nós, representando os atores (agentes, posições ou papéis) e arestas, representando as dependências entre os mesmos.

![i__sd](https://user-images.githubusercontent.com/14116020/27992013-bb6c5c06-645f-11e7-9c90-8883bce39840.png)

## Modelo SR (modelo de dependências estratégicas)
 
Enquanto o modelo SD trata apenas dos relacionamentos externos entre os atores, o modelo SR é utilizado para descrever os relacionamentos internos. Ele possibilita a avaliação das possíveis alternativas de definição do processo, investigado mais detalhadamente as razões existentes, ou intencionalidades, por trás das dependências entre os atores.

Assim como o SD, o modelo SR também é composto por ligações de dependência:

* **Means-ends**: As ligações de meio-fim indicam um relacionamento entre um nó fim e um meio para atingi-lo.

* **Decomposition**: Já as ligações de decomposição de tarefas ligam um nó de tarefa a seus nós componentes, que segundo [Yu 1995] podem ser outras tarefas, objetivos, recursos ou objetivos-soft, nesse diagrama foi utilizado dois tipos de decomposição de tarefas:

   - **AND e AND**: todas vão acontecer.

   - **AND e OR**: uma irá acontecer a outra pode ou não acontecer

   - **OR e OR**: uma das duas irá acontecer.

![i__sr](https://user-images.githubusercontent.com/14116020/36355761-e01fc084-14c6-11e8-84bb-438e3b96a197.png)

## Referências

Istar Wiki. Disponível em:  <http://istar.rwth-aachen.de/tiki-view_articles.php> Acesso em 17 de abril de 2017.
