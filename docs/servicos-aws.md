# Conceitos AWS - Cachorro Loko

Documentação dos serviços AWS utilizados no projeto e conceitos aprendidos.

## 🏗️ Arquitetura AWS

```
Internet → API Gateway → Lambda (Django) → RDS/Neon → S3 (Static Files)
```

## 🔐 IAM (Identity and Access Management)

### Conceitos Aplicados

#### Usuários e Políticas

- **Usuário IAM:** `zappa-deploy-user` para deploy automatizado
- **Políticas:** Permissões específicas para cada serviço
- **Princípio do menor privilégio:** Apenas permissões necessárias

#### Políticas Utilizadas

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "lambda:*",
        "apigateway:*",
        "s3:*",
        "iam:*",
        "cloudformation:*",
        "events:*"
      ],
      "Resource": "*"
    }
  ]
}
```

### Aprendizados

- **Credenciais de acesso:** Access Key ID + Secret Access Key
- **Profiles:** Múltiplas contas AWS no mesmo CLI
- **Roles:** Permissões temporárias para serviços

## 🪣 S3 (Simple Storage Service)

### Uso no Projeto

- **Bucket Zappa:** `zappa-cachorro-loko-backend`
- **Artefatos de deploy:** Código empacotado do Lambda
- **Static files:** Arquivos estáticos do Django

### Conceitos

- **Buckets:** Containers para objetos
- **Regiões:** Localização geográfica dos dados
- **ACL:** Controle de acesso aos objetos
- **Versioning:** Histórico de versões dos arquivos

### Configuração

```yaml
# zappa_settings.json
{
  "dev":
    { "s3_bucket": "zappa-cachorro-loko-backend", "aws_region": "sa-east-1" },
}
```

## ⚡ Lambda (Serverless Computing)

### Conceitos Aplicados

#### Function as a Service (FaaS)

- **Execução sob demanda:** Código roda apenas quando necessário
- **Auto-scaling:** Escala automaticamente com a demanda
- **Pay-per-use:** Cobrança por execução, não por tempo ocioso

#### Configuração Lambda

```python
# Runtime
"runtime": "python3.11"

# Memory e timeout
"memory_size": 512,
"timeout_seconds": 30

# Environment variables
"environment_variables": {
  "DB_ENGINE": "django.db.backends.postgresql",
  "DB_NAME": "neondb"
}
```

### Aprendizados

- **Cold start:** Tempo de inicialização da função
- **Warm start:** Execuções subsequentes mais rápidas
- **Concurrent executions:** Limite de execuções simultâneas
- **Dead letter queues:** Tratamento de falhas

## 🌐 API Gateway

### Conceitos Aplicados

#### RESTful API

- **Endpoints:** URLs para diferentes recursos
- **HTTP Methods:** GET, POST, PUT, DELETE
- **Status codes:** Respostas padronizadas
- **CORS:** Cross-Origin Resource Sharing

#### Configuração

```yaml
# Rotas configuradas
/health/ → Django health check
/api/auth/token/ → JWT authentication
/api/subscription/ → Subscription management
/admin/ → Django admin interface
```

### Aprendizados

- **API Keys:** Autenticação via chave
- **Usage plans:** Controle de uso da API
- **Throttling:** Limitação de requisições
- **Caching:** Cache de respostas
- **Custom domains:** Domínios personalizados

## 🗄️ Banco de Dados

### Neon.tech (PostgreSQL Serverless)

- **Serverless:** Sem gerenciamento de servidor
- **Auto-scaling:** Escala automaticamente
- **Connection pooling:** Reutilização de conexões
- **Backup automático:** Snapshots automáticos

### Configuração

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'neondb',
        'USER': 'neondb_owner',
        'PASSWORD': 'npg_UE8mhVOgqDZ2',
        'HOST': 'ep-icy-fire-achf0hnj-pooler.sa-east-1.aws.neon.tech',
        'PORT': '5432',
    }
}
```

## 🔧 Zappa (Deployment Tool)

### Conceitos Aplicados

#### Serverless Deployment

- **Packaging:** Empacotamento do código Django
- **Dependencies:** Instalação automática de dependências
- **Static files:** Coleta e upload de arquivos estáticos
- **Environment management:** Diferentes ambientes (dev, prod)

#### Comandos Utilizados

```bash
# Deploy inicial
zappa deploy dev

# Atualização
zappa update dev

# Comandos Django
zappa manage dev migrate
zappa manage dev createsuperuser

# Logs
zappa tail dev
```

### Aprendizados

- **Lambda layers:** Dependências compartilhadas
- **VPC configuration:** Rede virtual privada
- **Environment variables:** Configuração por ambiente
- **Rollback:** Reversão para versão anterior

## 📊 Monitoramento

### CloudWatch

- **Logs:** Logs de execução do Lambda
- **Metrics:** Métricas de performance
- **Alarms:** Alertas baseados em métricas
- **Dashboards:** Visualização de métricas

### Métricas Importantes

- **Invocations:** Número de execuções
- **Duration:** Tempo de execução
- **Errors:** Taxa de erro
- **Throttles:** Limitações de concorrência

## 💰 Custos

### Estimativa Mensal (Brasil - sa-east-1)

- **Lambda:** ~$0.20 (1M execuções)
- **API Gateway:** ~$3.50 (1M requests)
- **S3:** ~$0.50 (10GB storage)
- **Neon.tech:** $0 (plano gratuito)

**Total estimado:** ~$4.20/mês

### Otimizações

- **Connection pooling:** Reduzir conexões de banco
- **Caching:** Reduzir chamadas desnecessárias
- **Compression:** Reduzir tamanho dos payloads
- **Cold start optimization:** Manter função "quente"

## 🔒 Segurança

### Boas Práticas Aplicadas

- **Environment variables:** Credenciais em variáveis de ambiente
- **IAM roles:** Permissões mínimas necessárias
- **HTTPS:** Comunicação criptografada
- **CORS:** Controle de origem das requisições

### Configurações de Segurança

```python
# settings.py
ALLOWED_HOSTS = ["*"]  # Ajustar para domínio específico
CORS_ALLOW_ALL_ORIGINS = True  # Ajustar para origens específicas
DEBUG = False  # Desabilitar em produção
```

## 🚀 Próximos Passos

1. **CloudFront:** CDN para arquivos estáticos
2. **Route 53:** DNS personalizado
3. **WAF:** Web Application Firewall
4. **Secrets Manager:** Gerenciamento de credenciais
5. **X-Ray:** Tracing distribuído

## 📚 Referências

- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [API Gateway Documentation](https://docs.aws.amazon.com/apigateway/)
- [S3 Documentation](https://docs.aws.amazon.com/s3/)
- [IAM Documentation](https://docs.aws.amazon.com/iam/)
- [Zappa Documentation](https://github.com/Miserlou/Zappa)


