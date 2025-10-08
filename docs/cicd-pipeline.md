# Pipeline CI/CD - Cachorro Loko

Implementação de pipeline automatizado para deploy contínuo do projeto.

## 🎯 Objetivos do Pipeline

- **Deploy automático** do backend (Django + Zappa)
- **Deploy automático** do frontend (React + S3)
- **Testes automatizados** antes do deploy
- **Rollback automático** em caso de falha
- **Notificações** de status do deploy

## 🏗️ Arquitetura do Pipeline

```
Git Push → GitHub Actions → Testes → Deploy Backend → Deploy Frontend → Notificação
```

## 📋 Configuração GitHub Actions

### 1. **Estrutura de Arquivos**

```
.github/
└── workflows/
    ├── backend-deploy.yml
    ├── frontend-deploy.yml
    └── full-deploy.yml
```

### 2. **Backend Deploy (Django + Zappa)**

```yaml
# .github/workflows/backend-deploy.yml
name: Backend Deploy

on:
  push:
    branches: [main]
    paths: ["backend/**"]
  pull_request:
    branches: [main]
    paths: ["backend/**"]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          cd backend/api
          pip install -r requirements.txt

      - name: Run tests
        run: |
          cd backend/api
          python manage.py test

      - name: Lint code
        run: |
          cd backend/api
          flake8 .
          black --check .

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
      - uses: actions/checkout@v3

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: sa-east-1

      - name: Deploy to AWS
        run: |
          cd backend/api
          pip install zappa
          zappa update dev

      - name: Run migrations
        run: |
          cd backend/api
          zappa manage dev migrate

      - name: Notify deployment
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          channel: "#deployments"
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

### 3. **Frontend Deploy (React + S3)**

```yaml
# .github/workflows/frontend-deploy.yml
name: Frontend Deploy

on:
  push:
    branches: [main]
    paths: ["frontend/**"]
  pull_request:
    branches: [main]
    paths: ["frontend/**"]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: "18"
          cache: "npm"
          cache-dependency-path: frontend/package-lock.json

      - name: Install dependencies
        run: |
          cd frontend
          npm ci

      - name: Run tests
        run: |
          cd frontend
          npm test -- --coverage --watchAll=false

      - name: Lint code
        run: |
          cd frontend
          npm run lint

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
      - uses: actions/checkout@v3

      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: "18"
          cache: "npm"
          cache-dependency-path: frontend/package-lock.json

      - name: Install dependencies
        run: |
          cd frontend
          npm ci

      - name: Build React app
        run: |
          cd frontend
          npm run build

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: sa-east-1

      - name: Deploy to S3
        run: |
          aws s3 sync frontend/build/ s3://cachorro-loko-frontend --delete

      - name: Invalidate CloudFront
        run: |
          aws cloudfront create-invalidation --distribution-id ${{ secrets.CLOUDFRONT_DISTRIBUTION_ID }} --paths "/*"

      - name: Notify deployment
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          channel: "#deployments"
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

### 4. **Deploy Completo**

```yaml
# .github/workflows/full-deploy.yml
name: Full Deploy

on:
  push:
    branches: [main]
    paths: ["**"]
  workflow_dispatch:

jobs:
  backend:
    uses: ./.github/workflows/backend-deploy.yml

  frontend:
    uses: ./.github/workflows/frontend-deploy.yml

  notify:
    needs: [backend, frontend]
    runs-on: ubuntu-latest
    if: always()

    steps:
      - name: Notify final status
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          channel: "#deployments"
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
          fields: repo,message,commit,author,action,eventName,ref,workflow
```

## 🔐 Configuração de Secrets

### **GitHub Secrets Necessários**

```bash
# AWS Credentials
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...

# Slack Notifications
SLACK_WEBHOOK=https://hooks.slack.com/...

# CloudFront
CLOUDFRONT_DISTRIBUTION_ID=E1234567890

# Database (se necessário)
DB_HOST=ep-icy-fire-achf0hnj-pooler.sa-east-1.aws.neon.tech
DB_PASSWORD=npg_UE8mhVOgqDZ2
```

### **Como Configurar Secrets**

1. Acesse o repositório no GitHub
2. Vá em **Settings** → **Secrets and variables** → **Actions**
3. Clique em **New repository secret**
4. Adicione cada secret listado acima

## 🧪 Configuração de Testes

### **Backend (Django)**

```python
# backend/api/requirements-dev.txt
pytest==7.4.0
pytest-django==4.5.2
pytest-cov==4.1.0
flake8==6.0.0
black==23.7.0
```

```python
# backend/api/pytest.ini
[tool:pytest]
DJANGO_SETTINGS_MODULE = api.settings
python_files = tests.py test_*.py *_tests.py
addopts = --cov=. --cov-report=html --cov-report=term-missing
```

### **Frontend (React)**

```json
// frontend/package.json
{
  "scripts": {
    "test": "react-scripts test",
    "test:coverage": "react-scripts test --coverage --watchAll=false",
    "lint": "eslint src/",
    "lint:fix": "eslint src/ --fix"
  },
  "devDependencies": {
    "@testing-library/jest-dom": "^5.16.5",
    "@testing-library/react": "^13.4.0",
    "@testing-library/user-event": "^14.4.3",
    "eslint": "^8.45.0"
  }
}
```

## 🚀 Deploy Manual

### **Backend**

```bash
# Deploy manual
cd backend/api
zappa update dev

# Com rollback
zappa update dev --rollback

# Deploy para produção
zappa update production
```

### **Frontend**

```bash
# Build local
cd frontend
npm run build

# Deploy manual
aws s3 sync build/ s3://cachorro-loko-frontend --delete
aws cloudfront create-invalidation --distribution-id E1234567890 --paths "/*"
```

## 📊 Monitoramento do Pipeline

### **Métricas Importantes**

1. **Build Time:** Tempo total de build
2. **Test Coverage:** Cobertura de testes
3. **Deploy Success Rate:** Taxa de sucesso
4. **Rollback Frequency:** Frequência de rollbacks

### **Alertas Configurados**

- ❌ **Build Failure:** Falha nos testes
- ❌ **Deploy Failure:** Falha no deploy
- ⚠️ **High Test Time:** Testes demorando muito
- ⚠️ **Low Coverage:** Cobertura baixa

## 🔄 Estratégias de Deploy

### **1. Blue-Green Deployment**

```yaml
# Deploy em ambiente paralelo
- Deploy em 'staging'
- Testes de integração
- Switch para 'production'
- Rollback se necessário
```

### **2. Canary Deployment**

```yaml
# Deploy gradual
- 10% do tráfego para nova versão
- Monitorar métricas
- Aumentar gradualmente
- Rollback se problemas
```

### **3. Rolling Deployment**

```yaml
# Deploy por partes
- Deploy em batches
- Zero downtime
- Rollback automático
```

## 🛠️ Ferramentas Utilizadas

### **CI/CD**

- **GitHub Actions:** Orquestração do pipeline
- **AWS CLI:** Deploy para AWS
- **Zappa:** Deploy serverless

### **Testes**

- **pytest:** Testes Python
- **Jest:** Testes React
- **ESLint:** Linting JavaScript
- **Black:** Formatação Python

### **Deploy**

- **S3:** Hosting estático
- **CloudFront:** CDN
- **Lambda:** Backend serverless

## 📈 Otimizações

### **Performance**

- **Cache de dependências:** npm cache, pip cache
- **Build paralelo:** Jobs em paralelo
- **Artifacts:** Reutilização de builds

### **Custos**

- **Spot instances:** Para testes
- **Scheduled builds:** Apenas quando necessário
- **Cleanup:** Limpeza de recursos antigos

## 🔧 Troubleshooting

### **Problemas Comuns**

#### 1. **Deploy Falha**

```bash
# Verificar logs
zappa tail dev

# Verificar status
zappa status dev

# Rollback
zappa rollback dev
```

#### 2. **Testes Falham**

```bash
# Executar localmente
python manage.py test
npm test

# Verificar cobertura
pytest --cov=.
```

#### 3. **Build Lento**

- Verificar cache de dependências
- Otimizar Docker layers
- Usar runners mais rápidos

## 📚 Próximos Passos

1. **Implementar testes E2E** com Cypress
2. **Configurar monitoramento** com DataDog/New Relic
3. **Implementar feature flags** com LaunchDarkly
4. **Configurar backup automático** do banco
5. **Implementar security scanning** com Snyk

## 📖 Referências

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [AWS CLI Documentation](https://docs.aws.amazon.com/cli/)
- [Zappa Documentation](https://github.com/Miserlou/Zappa)
- [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/)
- [pytest Documentation](https://docs.pytest.org/)
