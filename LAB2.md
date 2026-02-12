# Apresentação Tecnológica

A equipe trabalhará com o framework de gestão scrum e kanbam para a nossa organização.

O projeto vai utilizar o LeafLet para mostrar o mapa, pois o nosso aplicativo pode cadastrar fretes contendo endereços. Esses endereços serão armazenados no Postgres com a Extensão do PostGis, que facilitará para nois a criação de buscas por geolocalização. Nosso sistema terá um chat, e para a comunicação será necessário um sistema de websocket com varias instancias, por isso precisaremos de um Redis, para guardar informação entre diversas instancias do sistema. O lucro do projeto será por via de anuncios, utilizando do sistema do google (GoogleAds).

Utilizaremos o FastAPI para a criação do serviço REST, sua vantagem de criação de documentação, validação e assincronismo nos garante uma boa velocidade de desenvolvimento, nos trazendo apenas o foco na parte de negócios.
O sistema tera um chat, no qual armazenará arquivos diferentes de texto no s3, utilizando de sdks prontas.
O FastAPI tambem nos disponibiliza o sistema de websocket para o chat. Utilizaremos o SQLModel para comunicação dos nossos modelos de dados onde poderemos consumir de forma performatica informações de localizações de fretes, junto do alembic para o versionamento do banco de dados e criação das migrations. Logging do python para a observabilidade, pydantic para a criação dos schemas da api para a documentação automatica e validação de dados juntos de validação de segurança, como verificar se o cpf é valido. Pydantic settings para utilizarmos os segredos de forma simples e com a sintaxe tipada do python. React Native para o app mobile. A arquitetura será organizada a partir de um Model-Controller-Routes-Services, onde temos modelos do sqlmodel, routes da api e serviçes para serviços externos. Utilizaremos o nomatim para facilitar e disponibilizar funcionalidades de endereços.

# Bibliotecas & Frameworks

- FastAPI (criação do serviço de REST API)
- SQLModel (criar os modelso de banco de dados utilizando a mesma sintaxe do pydantic)
- asyncpg (conectar no banco de forma assincrona)
- logging (logar)
- alembic (criar migrações no banco)
- pydantic (validar dados)
- pydantic-settings (criar e gerenciar os segredos da aplicação)
- React Native (Criação do código nativo usando o jsvascript)

# API DE TERCEIROS

- GoogleAds (Anuncios no aplicativo)
- Nomatim api (Para informações de endereços)
- Leaflet (Para o plot do mapa)
- s3 (Para o armazenamento de midias)

# Arquitetura

Model-Controller-Routes-Services

# Modelos e processos

- Scrum
- Kanban
