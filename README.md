# Cachorro Loko - Sistema de Assinaturas

Sistema de gerenciamento de assinaturas mensais (R$10/mês) para a comunidade Cachorro Loko, desenvolvido com Django + React e deploy serverless na AWS.

## 🏗️ Arquitetura

- **Backend:** Django + DRF + PostgreSQL (Neon.tech)
- **Frontend:** React + Axios
- **Deploy:** AWS Lambda + API Gateway (Zappa)
- **Banco:** PostgreSQL serverless (Neon.tech)
- **Desenvolvimento:** Docker Compose

## 🚀 Funcionalidades

- ✅ Autenticação JWT
- ✅ Sistema de assinatura mensal (último dia do mês)
- ✅ Dashboard com status e dias restantes
- ✅ Deploy serverless na AWS
- ✅ Banco PostgreSQL gratuito

## 📁 Estrutura do Projeto

```
cachorro-loko/
├── backend/
│   ├── api/                 # Django + DRF
│   └── infra/
│       └── docker-compose.yml
├── frontend/               # React App
├── docs/                   # Documentação
└── infra/                  # Infraestrutura
```

## 🛠️ Setup Local

### Pré-requisitos

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- AWS CLI configurado

### 1. Backend (Django + PostgreSQL)

```bash
cd backend/api
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Configurar banco local
cp .env.example .env
# Editar .env com credenciais do PostgreSQL local

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### 2. Frontend (React)

```bash
cd frontend
npm install
npm start
```

### 3. Banco de Dados (Docker)

```bash
cd backend/infra
docker-compose up -d
```

Acesse:

- **API:** http://127.0.0.1:8000
- **Frontend:** http://localhost:3000
- **pgAdmin:** http://localhost:5050

## 🌐 Deploy AWS

### Deploy Backend (Zappa)

```bash
cd backend/api
zappa deploy dev
zappa manage dev migrate
zappa manage dev createsuperuser
```

### URLs de Produção

- **API:** https://nxgnr11c1a.execute-api.sa-east-1.amazonaws.com/dev
- **Health:** https://nxgnr11c1a.execute-api.sa-east-1.amazonaws.com/dev/health/

## 📚 Documentação

- [Setup Detalhado](docs/setup.md)
- [Conceitos AWS](docs/aws-concepts.md)
- [Tradicional vs Serverless](docs/traditional-vs-serverless.md)
- [Pipeline CI/CD](docs/cicd-pipeline.md)

## 🔧 Tecnologias

### Backend

- Django 5.1
- Django REST Framework
- PostgreSQL (Neon.tech)
- Zappa (AWS Lambda)
- JWT Authentication

### Frontend

- React 18
- Axios
- React Router DOM

### Infraestrutura

- AWS Lambda
- API Gateway
- S3 (Zappa)
- Neon.tech (PostgreSQL)
- Docker Compose

## 📝 Próximos Passos

- [ ] Integração Stripe (pagamentos)
- [ ] Deploy frontend (S3 + CloudFront)
- [ ] Pipeline CI/CD
- [ ] Testes automatizados
- [ ] Monitoramento (CloudWatch)

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
