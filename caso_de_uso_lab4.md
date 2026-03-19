```plantUML
@startuml
left to right direction
:Caminhoneiro: as A1
:Criador de Demanda: as A2
(Candidatar a \numa demanda) as C1
(Criar \numa demanda) as C2
(Enviar Mensagen \nà outra parte ) as C3
(Acessar as \n mensagem da conversa com\n o outro usuario) as C4
(Buscar Demandas) as C5
(Editar Demanda) as C6
(Ver candidaturas) as C7
(Selecionar caminhoneiro \npara a demanda) as C8

A1 --> C1
A1 --> C3
A1 --> C4
A1 --> C5

C2 <-- A2
C3 <-- A2
C4 <-- A2
C6 <-- A2
C7 <-- A2
C8 <-- A2








@enduml

```
