```plantUML
@startuml
skinparam componentStyle uml2

' Definição das Interfaces do Sistema (Lollipops)

' Definição dos Componentes
component "Notificações" as CompNot
interface "I.Mensagem" as IMsg
component "Chat" as CompChat
interface "I.Chat" as IChat
component "Candidaturas" as CompCan
interface "I.Candidatura" as ICan
component "Demandas" as CompDem
interface "I.Demandas" as IDem


CompChat -left- IChat
CompCan -down- ICan
CompCan -( IDem
CompNot -up- IMsg
CompNot -( ICan
CompDem -( IChat
CompDem -( IMsg
CompDem -( ICan
CompDem -up- IDem


@enduml
```
