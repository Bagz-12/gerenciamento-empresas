# Plano de Deploy — Sistema de Gerenciamento de Empresas

**Disciplinas:** Desenvolvimento Python + Cloud Computing  
**Professor:** Michel Santos  
**Aluno:** Gabriel Lima  

---

## 1. Visão Geral do Projeto

O projeto consiste em um sistema web de gerenciamento de empresas e sócios, desenvolvido com **FastAPI** (backend Python) e **Vue 3** (frontend), com deploy automatizado em ambiente de nuvem utilizando containers Docker.

### Tecnologias Utilizadas

| Camada | Tecnologia |
|--------|-----------|
| Backend | Python 3.13 + FastAPI |
| Frontend | Vue 3 + Vite + Nginx |
| Banco de Dados | PostgreSQL 16 (DigitalOcean Managed Database) |
| Autenticação | GitHub OAuth 2.0 |
| Containers | Docker + Docker Compose |
| Registry de Imagens | Docker Hub |
| CI/CD | GitHub Actions |
| Infraestrutura | DigitalOcean (Droplet + Managed Database) |

---

## 2. Arquitetura da Solução

```
┌─────────────────────────────────────────────────────────────┐
│                        DESENVOLVEDOR                        │
│                    git push origin main                     │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                      GITHUB                                 │
│                                                             │
│   Repositório: Bagz-12/gerenciamento-empresas               │
│   Branch: main                                              │
│                                                             │
│   ┌─────────────────────────────────────────────────────┐   │
│   │              GITHUB ACTIONS (CI/CD)                 │   │
│   │                                                     │   │
│   │  Job 1: Build & Push                                │   │
│   │  - Checkout do código                               │   │
│   │  - Build imagem backend (FastAPI)                   │   │
│   │  - Build imagem frontend (Vue 3 + Nginx)            │   │
│   │  - Push das imagens para o Docker Hub               │   │
│   │                                                     │   │
│   │  Job 2: Deploy                                      │   │
│   │  - Conecta no servidor via SSH                      │   │
│   │  - Puxa novas imagens do Docker Hub                 │   │
│   │  - Reinicia os containers                           │   │
│   └─────────────────────────────────────────────────────┘   │
└──────────────┬──────────────────────┬───────────────────────┘
               │                      │
               ▼                      ▼
┌──────────────────────┐  ┌───────────────────────────────────┐
│      DOCKER HUB      │  │        DIGITALOCEAN               │
│                      │  │                                   │
│  bagz12/empresas-    │  │  ┌─────────────────────────────┐  │
│  backend:latest      │  │  │   DROPLET (Servidor)        │  │
│                      │  │  │                             │  │
│  bagz12/empresas-    │  │  │   ┌─────────────────────┐   │  │
│  frontend:latest     │  │  │   │  Container Backend  │   │  │
│                      │  │  │   │  FastAPI :8000       │   │  │
└──────────────────────┘  │  │   └─────────────────────┘   │  │
                          │  │   ┌─────────────────────┐   │  │
                          │  │   │  Container Frontend │   │  │
                          │  │   │  Nginx :80          │   │  │
                          │  │   └─────────────────────┘   │  │
                          │  └─────────────────────────────┘  │
                          │                                   │
                          │  ┌─────────────────────────────┐  │
                          │  │  MANAGED DATABASE           │  │
                          │  │  PostgreSQL 16 :25060       │  │
                          │  └─────────────────────────────┘  │
                          └───────────────────────────────────┘
```

---

## 3. Fluxo do CI/CD

### Gatilho
O pipeline é disparado automaticamente a cada `push` na branch `main`.

### Job 1 — Build & Push (equivalente ao ACR no Azure)

```
1. Checkout do código-fonte
2. Autenticação no Docker Hub
3. Build da imagem Docker do Backend
   - Contexto: ./backend
   - Dockerfile: ./backend/Dockerfile
   - Tags: bagz12/empresas-backend:<sha> e bagz12/empresas-backend:latest
4. Push da imagem do Backend para o Docker Hub
5. Build da imagem Docker do Frontend
   - Contexto: ./frontend
   - Dockerfile: ./frontend/Dockerfile
   - Tags: bagz12/empresas-frontend:<sha> e bagz12/empresas-frontend:latest
6. Push da imagem do Frontend para o Docker Hub
```

### Job 2 — Deploy (equivalente ao Web App for Containers no Azure)

```
1. Decodificar chave SSH (armazenada em base64 nos Secrets)
2. Adicionar servidor ao known_hosts via ssh-keyscan
3. Conectar ao servidor via SSH
4. Criar arquivo .env com as variáveis de ambiente
5. docker compose pull  →  baixa as novas imagens do Docker Hub
6. docker compose up -d →  sobe os containers em background
7. docker system prune  →  limpa imagens antigas
```

---

## 4. Infraestrutura

### Servidor de Aplicação (Droplet DigitalOcean)
- **SO:** Ubuntu 24.04 LTS
- **Região:** New York (nyc1)
- **Plano:** Basic (1 vCPU, 1GB RAM)
- **IP Público:** 137.184.56.103
- **Serviços rodando:** Docker, Docker Compose

### Banco de Dados (Managed Database DigitalOcean)
- **Engine:** PostgreSQL 16
- **Região:** New York (nyc1)
- **Acesso:** Via connection string com SSL obrigatório (`sslmode=require`)
- **Isolamento:** Banco separado do servidor de aplicação

### Registry de Imagens (Docker Hub)
- **Repositório backend:** `bagz12/empresas-backend`
- **Repositório frontend:** `bagz12/empresas-frontend`
- **Estratégia de tags:** SHA do commit + `latest`

---

## 5. Variáveis de Ambiente e Secrets

### Secrets configurados no GitHub Actions

| Secret | Descrição |
|--------|-----------|
| `DOCKER_USERNAME` | Usuário do Docker Hub |
| `DOCKER_PASSWORD` | Token de acesso do Docker Hub (Read & Write) |
| `SSH_HOST` | IP do servidor DigitalOcean |
| `SSH_USER` | Usuário SSH do servidor |
| `SSH_PRIVATE_KEY` | Chave privada SSH em base64 |
| `DATABASE_URL` | Connection string do PostgreSQL remoto |
| `GH_CLIENT_ID` | Client ID do GitHub OAuth App |
| `GH_CLIENT_SECRET` | Client Secret do GitHub OAuth App |

### Variáveis de ambiente dos containers

| Variável | Container | Descrição |
|----------|-----------|-----------|
| `DATABASE_URL` | Backend | URL de conexão com o banco |
| `GH_CLIENT_ID` | Backend | ID do app OAuth GitHub |
| `GH_CLIENT_SECRET` | Backend | Secret do app OAuth GitHub |

---

## 6. Containers e Dockerfiles

### Backend (FastAPI)

```dockerfile
FROM python:3.13-slim
WORKDIR /app
RUN apt-get update && apt-get install -y libpq-dev gcc
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend (Vue 3 + Nginx)

```dockerfile
# Estágio 1: Build do Vue
FROM node:20-alpine AS builder
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
RUN npm run build

# Estágio 2: Servir com Nginx
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
```

### Docker Compose (Produção)

```yaml
services:
  backend:
    image: bagz12/empresas-backend:latest
    environment:
      DATABASE_URL: ${DATABASE_URL}
      GH_CLIENT_ID: ${GH_CLIENT_ID}
      GH_CLIENT_SECRET: ${GH_CLIENT_SECRET}
    ports:
      - "8000:8000"

  frontend:
    image: bagz12/empresas-frontend:latest
    ports:
      - "80:80"
    depends_on:
      - backend
```

---

## 7. Funcionalidades da Aplicação

### CRUD de Empresas
| Operação | Método | Rota |
|----------|--------|------|
| Criar | POST | `/empresas` |
| Listar / Buscar | GET | `/empresas?busca=termo` |
| Buscar por ID | GET | `/empresas/{id}` |
| Atualizar | PUT | `/empresas/{id}` |
| Remover | DELETE | `/empresas/{id}` |

### CRUD de Sócios
| Operação | Método | Rota |
|----------|--------|------|
| Criar | POST | `/socios` |
| Listar | GET | `/socios` |
| Listar por empresa | GET | `/socios/empresa/{id}` |
| Buscar por ID | GET | `/socios/{id}` |
| Atualizar | PUT | `/socios/{id}` |
| Remover | DELETE | `/socios/{id}` |

### Autenticação GitHub OAuth
| Rota | Descrição |
|------|-----------|
| `GET /auth/github/login` | Inicia o fluxo OAuth |
| `GET /auth/github/callback` | Recebe o código e retorna o token |
| `GET /auth/github/user` | Retorna dados do usuário autenticado |

---

## 8. URL Pública

| Serviço | URL |
|---------|-----|
| Frontend | http://137.184.56.103 |
| Backend API | http://137.184.56.103:8000 |
| Documentação interativa | http://137.184.56.103:8000/docs |
| Login GitHub | http://137.184.56.103:8000/auth/github/login |
