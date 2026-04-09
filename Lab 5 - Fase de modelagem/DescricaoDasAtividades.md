## Descrição das atividades

| Tarefa                                  | Descrição                                                                                                                                    |
| --------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| Informar dados da demanda               | O criador de demandas preenche as informações da demanda (origem, destino, carga, prazo e demais dados necessários) para iniciar o cadastro. |
| Ver candidaturas                        | O criador de demandas acessa a lista de caminhoneiros que se candidataram à sua demanda.                                                     |
| Selecionar caminhoneiro                 | O criador de demandas escolhe um caminhoneiro entre os candidatos disponíveis.                                                               |
| Aceitar candidatura (decisão)           | O criador decide se confirma a candidatura selecionada; se não aceitar, o fluxo é encerrado ou retorna para nova seleção.                    |
| Validar dados da demanda                | O sistema verifica se os campos obrigatórios e formatos dos dados informados estão corretos.                                                 |
| Validar informações (decisão)           | Ponto de decisão do sistema para separar dados válidos e inválidos após a validação.                                                         |
| Enviar alerta ao usuário                | Quando houver erro de preenchimento, o sistema envia uma mensagem indicando o problema para correção.                                        |
| Buscar latitude e longitude do endereço | Com os dados válidos, o sistema consulta coordenadas geográficas dos endereços informados.                                                   |
| Cadastrar demanda no banco              | O sistema grava a demanda validada no banco de dados.                                                                                        |
| Buscar demanda                          | O caminhoneiro consulta demandas disponíveis de acordo com os filtros ou região.                                                             |
| Candidatar-se (decisão)                 | O caminhoneiro decide se quer se candidatar à demanda encontrada; se não, o fluxo é finalizado.                                              |
| Cadastrar candidatura no banco          | Quando o caminhoneiro confirma interesse, o sistema registra a candidatura no banco de dados.                                                |
| Enviar notificação para criador         | O sistema notifica o criador de demandas sobre nova candidatura recebida.                                                                    |
| Enviar notificação para caminhoneiro    | O sistema notifica o caminhoneiro sobre o resultado da candidatura (aceite/recusa).        