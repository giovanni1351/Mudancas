## Regras de Negócio

- **RN01**: Somente usuários com perfil **Caminhoneiro** podem se candidatar a uma demanda.
- **RN02**: Somente o **Criador de Demanda** proprietário pode editar sua demanda.
- **RN03**: A troca de mensagens só pode ocorrer entre partes envolvidas na mesma demanda.
- **RN04**: Um caminhoneiro pode realizar apenas **uma candidatura por demanda**.
- **RN05**: Uma demanda só pode ser publicada com origem, destino, tipo de carga e prazo preenchidos.

## Requisitos Não Funcionais

- **RNF01**: O sistema deve manter disponibilidade mínima de **99,5%** ao mês.
- **RNF02**: A busca de demandas deve responder em até **2 segundos** para 95% das requisições.
- **RNF03**: O sistema deve proteger dados sensíveis com criptografia em trânsito (**HTTPS/TLS**) e em repouso.
- **RNF04**: O sistema deve registrar logs de auditoria de ações críticas por no mínimo **12 meses**.
- **RNF05**: A interface deve ser responsiva e compatível com dispositivos móveis modernos.
