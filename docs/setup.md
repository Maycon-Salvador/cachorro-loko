# Setup Detalhado - Cachorro Loko

Este documento detalha o processo de configuração e os conceitos aplicados no projeto.

## 🐳 Docker + Django + PostgreSQL

### Conceitos Aplicados

#### Docker Compose

- **Orquestração de containers:** Múltiplos serviços (PostgreSQL + pgAdmin) em um único arquivo
- **Networking:** Containers se comunicam via rede interna
- **Volumes:** Persistência de dados do PostgreSQL
- **Environment variables:** Configuração via variáveis de ambiente

#### PostgreSQL

- **Banco relacional:** Estrutura de tabelas com relacionamentos
- **ACID:** Transações seguras e consistentes
- **Índices:** Performance otimizada para consultas
- **Migrations:** Versionamento do schema do banco

### Configuração Docker

```yaml
version: "3.9"
services:
  db:
    image: postgres:14
    environment:
      POSTGRES_DB: cachorro_loko
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - db_data:/var/lib/postgresql/data
```

**Conceitos:**

- **Image:** PostgreSQL 14 oficial do Docker Hub
- **Environment:** Variáveis de configuração do banco
- **Ports:** Mapeamento de porta (host:container)
- **Volumes:** Dados persistem entre restarts

### Django + PostgreSQL

#### Configuração de Banco

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }
}
```

**Conceitos:**

- **Environment variables:** Configuração flexível por ambiente
- **Database engine:** Driver específico para PostgreSQL
- **Connection pooling:** Reutilização de conexões
- **SSL/TLS:** Conexão segura em produção

## 🔧 Processo de Setup

### 1. Preparação do Ambiente

```bash
# Clone do repositório
git clone <repo-url>
cd cachorro-loko

# Criação de ambiente virtual
python -m venv backend/api/.venv
backend/api/.venv/Scripts/activate
```

### 2. Configuração do Banco

```bash
# Iniciar containers
cd backend/infra
docker-compose up -d

# Verificar status
docker-compose ps
```

### 3. Configuração do Django

```bash
cd backend/api

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env
# Editar .env com credenciais locais

# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser
```

### 4. Configuração do Frontend

```bash
cd frontend
npm install
npm start
```

## 🧪 Testes de Funcionamento

### Backend

```bash
# Testar API
curl http://127.0.0.1:8000/health/

# Testar autenticação
curl -X POST http://127.0.0.1:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"senha"}'
```

### Frontend

- Acesse http://localhost:3000
- Faça login com credenciais criadas
- Verifique dashboard com status da assinatura

### Banco de Dados

- Acesse http://localhost:5050 (pgAdmin)
- Login: admin@local / admin
- Conecte ao servidor PostgreSQL local

## 🔍 Troubleshooting

### Problemas Comuns

#### 1. Erro de Conexão com PostgreSQL

```bash
# Verificar se container está rodando
docker-compose ps

# Ver logs do container
docker-compose logs db

# Reiniciar containers
docker-compose restart
```

#### 2. Erro de Migração

```bash
# Resetar migrações (CUIDADO: apaga dados)
python manage.py migrate --fake-initial

# Aplicar migrações específicas
python manage.py migrate subscriptions
```

#### 3. Erro de Dependências

```bash
# Atualizar pip
python -m pip install --upgrade pip

# Reinstalar dependências
pip install -r requirements.txt --force-reinstall
```

## 📊 Monitoramento

### Logs do Django

```bash
# Logs detalhados
python manage.py runserver --verbosity=2

# Logs de SQL
python manage.py runserver --settings=api.settings_debug
```

### Logs do Docker

```bash
# Logs em tempo real
docker-compose logs -f

# Logs específicos
docker-compose logs db
docker-compose logs pgadmin
```

## 🚀 Próximos Passos

1. **Configurar ambiente de produção**
2. **Implementar testes automatizados**
3. **Configurar monitoramento**
4. **Documentar APIs**
5. **Implementar CI/CD**

## 📚 Referências

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Django Database Configuration](https://docs.djangoproject.com/en/stable/ref/settings/#databases)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Django REST Framework](https://www.django-rest-framework.org/)
