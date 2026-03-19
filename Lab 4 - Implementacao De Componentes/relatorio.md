# Mudanças - Implementação de Componentes
## Descrição dos Componentes
**Demanda**
Responsável por gerenciar as demandas de transporte, incluindo validação, registro, busca, detalhamento e associação de caminhoneiros às demandas.

**Candidatura**
Gerencia as candidaturas dos caminhoneiros às demandas, realizando validação, registro e exibição da lista de candidatos para uma demanda específica.

## Interfaces Fornecidas
- ``DemandaService``: Interface abstrata que define os métodos essenciais para o componente Demanda.
- ``CandidaturaService``: Interface abstrata que define os métodos essenciais para o componente Candidatura.

## Interfaces Requeridas
- O componente ``Candidatura`` requer uma instância de ``Demanda`` para associar candidaturas às demandas.

## Comunicação entre os Componentes
A comunicação ocorre por meio de interfaces abstratas. O componente ``Candidatura`` recebe uma instância de ``Demanda`` em seu construtor, permitindo interações sem dependência direta da implementação. Os métodos definidos nas interfaces garantem que a comunicação seja feita apenas por contratos, evitando dependências concretas.

## Justificativa para Evitar Acoplamento Direto
O acoplamento direto foi evitado utilizando interfaces abstratas (``DemandaService`` e ``CandidaturaService``). Os componentes dependem apenas das interfaces, não das implementações concretas, permitindo flexibilidade, testes e manutenção facilitada.

## Instruções para execução

- Certifique-se de ter python instalado
- rode o comando: `python '.\Lab 4 - Implementacao De Componentes\main.py'`