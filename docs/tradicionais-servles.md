# Tradicional vs Serverless

Comparativo direto entre hospedagem tradicional (VM/containers) e serverless (AWS Lambda).

## Quando usar

- Tradicional: apps com tráfego constante, processos longos, controle de SO/rede, dependências do sistema.
- Serverless: APIs/eventos intermitentes, tráfego variável, time pequeno de ops, custo sob demanda.

## Vantagens

- Tradicional

  - Controle total de runtime, SO e rede (VPC, portas, daemons).
  - Previsibilidade de performance (recursos dedicados).
  - Suporta jobs longos e serviços em tempo real (websockets dedicados).

- Serverless
  - Sem gerenciar servidor; escala automática.
  - Paga por execução; ótimo para uso intermitente.
  - Deploy simples (ex.: Zappa) e fácil integração com AWS (API Gateway, S3, CloudWatch).

## Desvantagens

- Tradicional

  - Custo base mesmo ocioso; precisa gerenciar patches, capacity e autoscaling.
  - Provisionamento mais lento e mais responsabilidade de segurança.

- Serverless
  - Cold start e limites de tempo/memória.
  - Debug local e observabilidade podem ser mais chatos.
  - Vendor lock-in maior (gatilhos/serviços específicos da nuvem).

## Custos (regra prática)

- Tráfego baixo/irregular → Serverless tende a ser mais barato.
- Tráfego alto/constante → Máquinas/containers com autoscaling podem sair melhor.

## Exemplos

- Tradicional: processamento de vídeo longo, serviços com conexões persistentes, sistemas que exigem drivers nativos específicos.
- Serverless: APIs REST, webhooks, tarefas assíncronas, rotinas agendadas.

## No projeto

- Backend publicado com Zappa (Lambda + API Gateway).
- Banco gerenciado fora da função (Neon.tech).
- Logs/monitoramento via CloudWatch; migrações com `zappa manage`.
