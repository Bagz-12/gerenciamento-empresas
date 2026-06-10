# Sistema de Gerenciamento de Empresas

API RESTful com **FastAPI + PostgreSQL** e frontend em **Vue 3**.  
Deploy automatizado com **Docker + GitHub Actions + Docker Hub + DigitalOcean**.

---

## Arquitetura de Deploy

```
Push no GitHub (main)
        ↓
GitHub Actions
        ↓
Build das imagens Docker (backend + frontend)
        ↓
Push para Docker Hub (registry de imagens)
        ↓
SSH no servidor DigitalOcean
        ↓
docker compose pull + up (containers sobem com as novas imagens)
```

---

## Tecnologias Utilizadas

| Camada | Tecnologia |
|--------|-----------|
| **Backend** | Python 3.13 + FastAPI |
| **Frontend** | Vue 3 + Vite + Nginx |
| **Banco de Dados** | PostgreSQL 16 |
| **Autenticação** | GitHub OAuth |
| **Containers** | Docker + Docker Compose |
| **Registry** | Docker Hub |
| **CI/CD** | GitHub Actions |
| **Cloud** | DigitalOcean (Droplet + Managed Database) |

---

## Estrutura do Projeto

```
gerenciamento-empresas/
├── .github/
│   └── workflows/
│       └── deploy.yml          # Pipeline CI/CD
├── backend/
│   ├── main.py                 # Classe Application (entry point)
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── database.py         # Classe DatabaseConfig (Singleton)
│       ├── models.py           # Classes Empresa e Socio (SQLAlchemy ORM)
│       ├── schemas.py          # Classes Pydantic (validação de dados)
│       ├── utils/
│       │   └── cnpj.py         # Classe CnpjValidator
│       ├── repositories/
│       │   ├── base_repository.py     # Classe abstrata BaseRepository
│       │   ├── empresa_repository.py  # Classe EmpresaRepository
│       │   └── socio_repository.py    # Classe SocioRepository
│       ├── services/
│       │   ├── empresa_service.py     # Classe EmpresaService
│       │   └── socio_service.py       # Classe SocioService
│       └── routers/
│           ├── auth.py         # Autenticação GitHub OAuth
│           ├── empresas.py     # Rotas CRUD de Empresas
│           └── socios.py       # Rotas CRUD de Sócios
└── frontend/
    ├── Dockerfile
    ├── nginx.conf
    ├── package.json
    └── src/
        ├── main.js
        ├── App.vue
        ├── router/index.js
        ├── assets/styles.css
        ├── utils/
        │   ├── cnpj.js         # Validação de CNPJ no frontend
        │   └── cpf.js          # Validação de CPF no frontend
        ├── services/
        │   ├── ApiClient.js    # Classe base ApiClient
        │   ├── EmpresaService.js
        │   └── SocioService.js
        ├── views/
        │   ├── EmpresaListView.vue
        │   ├── EmpresaFormView.vue
        │   └── EmpresaDetailView.vue
        └── components/
            └── ConfirmModal.vue
```

---

## Pipeline CI/CD

O pipeline é disparado automaticamente a cada push na branch `main` e executa dois jobs:

**Job 1 — Build & Push**
- Faz o build das imagens Docker do backend e frontend
- Publica as imagens no Docker Hub com a tag do commit e `latest`

**Job 2 — Deploy**
- Conecta no servidor via SSH
- Puxa as novas imagens do Docker Hub
- Reinicia os containers com `docker compose up -d`

### Secrets necessários no GitHub

| Secret | Descrição |
|--------|-----------|
| `DOCKER_USERNAME` | Usuário do Docker Hub |
| `DOCKER_PASSWORD` | Token de acesso do Docker Hub |
| `SSH_HOST` | IP do servidor DigitalOcean |
| `SSH_USER` | Usuário SSH (ex: root) |
| `SSH_PRIVATE_KEY` | Chave privada SSH em base64 |
| `GH_CLIENT_ID` | Client ID do GitHub OAuth App |
| `GH_CLIENT_SECRET` | Client Secret do GitHub OAuth App |

---

## Como Executar Localmente

### Pré-requisitos
- Docker e Docker Compose instalados

### Subir todos os serviços

```bash
docker compose up --build
```

| Serviço | URL |
|---------|-----|
| Frontend | http://localhost |
| Backend API | http://localhost:8000 |
| Documentação | http://localhost:8000/docs |

---

## Arquitetura OOP

| Camada | Classe(s) | Responsabilidade |
|--------|-----------|-----------------|
| **Models** | `Empresa`, `Socio` | Mapeamento ORM das tabelas |
| **Schemas** | `EmpresaCreate`, `EmpresaUpdate`, etc. | Validação Pydantic de entrada/saída |
| **Utils** | `CnpjValidator` | Algoritmo de validação do CNPJ |
| **Repository** | `BaseRepository` → `EmpresaRepository`, `SocioRepository` | Acesso ao banco (herança) |
| **Service** | `EmpresaService`, `SocioService` | Regras de negócio |
| **Routers** | `APIRouter` (FastAPI) | Endpoints HTTP |
| **Config** | `DatabaseConfig`, `Application` | Configuração e montagem da app |
| **Frontend Services** | `ApiClient` → `EmpresaService`, `SocioService` | Comunicação com a API (herança) |

---

## Endpoints da API

### Autenticação
| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/auth/github/login` | Inicia fluxo OAuth com GitHub |
| `GET` | `/auth/github/callback` | Callback do GitHub OAuth |
| `GET` | `/auth/github/user` | Retorna dados do usuário autenticado |

### Empresas
| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/empresas` | Criar empresa (valida CNPJ) |
| `GET` | `/empresas?busca=termo` | Listar / buscar por nome ou CNPJ |
| `GET` | `/empresas/{id}` | Buscar por ID (inclui sócios) |
| `PUT` | `/empresas/{id}` | Atualizar empresa |
| `DELETE` | `/empresas/{id}` | Remover empresa |

### Sócios
| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/socios` | Adicionar sócio |
| `GET` | `/socios` | Listar todos |
| `GET` | `/socios/empresa/{id}` | Listar por empresa |
| `GET` | `/socios/{id}` | Buscar por ID |
| `PUT` | `/socios/{id}` | Atualizar sócio |
| `DELETE` | `/socios/{id}` | Remover sócio |
