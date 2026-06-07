# Sistema de Gerenciamento de Empresas

API RESTful com **FastAPI + PostgreSQL** e frontend em **Vue 3**.  
Desenvolvido com **Programação Orientada a Objetos** em toda a stack.

---

## Estrutura do Projeto

```
trabalho python/
├── backend/
│   ├── main.py                        # Classe Application (entry point)
│   ├── requirements.txt
│   ├── .env.example
│   └── app/
│       ├── database.py                # Classe DatabaseConfig (Singleton)
│       ├── models.py                  # Classes Empresa e Socio (SQLAlchemy ORM)
│       ├── schemas.py                 # Classes Pydantic (validação de dados)
│       ├── utils/
│       │   └── cnpj.py                # Classe CnpjValidator
│       ├── repositories/
│       │   ├── base_repository.py     # Classe abstrata BaseRepository (genérica)
│       │   ├── empresa_repository.py  # Classe EmpresaRepository
│       │   └── socio_repository.py    # Classe SocioRepository
│       ├── services/
│       │   ├── empresa_service.py     # Classe EmpresaService (regras de negócio)
│       │   └── socio_service.py       # Classe SocioService
│       └── routers/
│           ├── empresas.py            # Rotas CRUD de Empresas
│           └── socios.py              # Rotas CRUD de Sócios
└── frontend/
    ├── index.html
    ├── vite.config.js
    ├── package.json
    └── src/
        ├── main.js
        ├── App.vue
        ├── router/index.js
        ├── assets/styles.css
        ├── utils/
        │   └── cnpj.js                # Classe CnpjUtil (validação no frontend)
        ├── services/
        │   ├── ApiClient.js           # Classe base ApiClient
        │   ├── EmpresaService.js      # Classe EmpresaService (herda ApiClient)
        │   └── SocioService.js        # Classe SocioService (herda ApiClient)
        ├── views/
        │   ├── EmpresaListView.vue    # Lista com barra de busca
        │   ├── EmpresaFormView.vue    # Formulário criar/editar
        │   └── EmpresaDetailView.vue  # Detalhes + gerenciar sócios
        └── components/
            └── ConfirmModal.vue
```

---

## Como Executar

### Pré-requisitos
- Python 3.11+
- Node.js 18+
- PostgreSQL rodando localmente

### 1. Banco de Dados

```sql
CREATE DATABASE empresas_db;
```

### 2. Backend

```bash
cd backend

# Crie e ative o ambiente virtual
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac

# Instale as dependências
pip install -r requirements.txt

# Configure o banco (copie e edite se necessário)
copy .env.example .env

# Inicie o servidor (as tabelas são criadas automaticamente)
uvicorn main:app --reload
```

Acesse a documentação interativa em: **http://localhost:8000/docs**

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

Acesse o sistema em: **http://localhost:5173**

---

## Arquitetura OOP

| Camada | Classe(s) | Responsabilidade |
|--------|-----------|-----------------|
| **Models** | `Empresa`, `Socio` | Mapeamento ORM das tabelas |
| **Schemas** | `EmpresaCreate`, `EmpresaUpdate`, etc. | Validação Pydantic de entrada/saída |
| **Utils** | `CnpjValidator` | Algoritmo de validação do CNPJ |
| **Repository** | `BaseRepository` (abstrata) → `EmpresaRepository`, `SocioRepository` | Acesso ao banco (herança) |
| **Service** | `EmpresaService`, `SocioService` | Regras de negócio, orquestra repositórios |
| **Routers** | `APIRouter` (FastAPI) | Endpoints HTTP, injeta serviços via DI |
| **Config** | `DatabaseConfig`, `Application` | Configuração e montagem da app |
| **Frontend Services** | `ApiClient` → `EmpresaService`, `SocioService` | Comunicação com a API (herança) |
| **Frontend Utils** | `CnpjUtil` | Validação e máscara de CNPJ no browser |

---

## Endpoints da API

### Empresas
| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/empresas` | Criar empresa (valida CNPJ) |
| `GET` | `/empresas?busca=termo` | Listar / buscar por nome ou CNPJ |
| `GET` | `/empresas/{id}` | Buscar por ID (inclui sócios) |
| `PUT` | `/empresas/{id}` | Atualizar empresa |
| `DELETE` | `/empresas/{id}` | Remover empresa (cascade sócios) |

### Sócios
| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/socios` | Adicionar sócio |
| `GET` | `/socios` | Listar todos |
| `GET` | `/socios/empresa/{id}` | Listar por empresa |
| `GET` | `/socios/{id}` | Buscar por ID |
| `PUT` | `/socios/{id}` | Atualizar sócio |
| `DELETE` | `/socios/{id}` | Remover sócio |
