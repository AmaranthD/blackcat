# 🏗️ BlackCat Architecture

Este documento explica como o BlackCat foi construído e por que.

---

## Stack Tecnológico

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  🐻 FastAPI                                            │
│  └── Framework web Python moderno e rápido            │
│      ├── Validação automática com Pydantic            │
│      ├── Documentação automática (Swagger UI)         │
│      └── Suporte a async/await                        │
│                                                         │
│  🗄️ SQLAlchemy ORM                                     │
│  └── Mapeamento objeto-relacional                     │
│      ├── Escreve SQL automaticamente                  │
│      ├── Suporte a múltiplos bancos                   │
│      └── Relacionamentos automáticos                  │
│                                                         │
│  🐘 PostgreSQL                                        │
│  └── Banco de dados robusto                          │
│      ├── Suporte a UUIDs nativamente                  │
│      ├── Índices para performance                     │
│      └── Transações ACID                             │
│                                                         │
│  🐋 Docker                                            │
│  └── Containerização                                 │
│      ├── Mesma app em dev e produção                 │
│      ├── Docker Compose para orquestração            │
│      └── Isolamento de ambientes                     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## Por que essas tecnologias?

### FastAPI
- ✅ Rápida (uma das mais rápidas em Python)
- ✅ Validação automática de dados
- ✅ Documentação interativa (Swagger UI)
- ✅ Fácil de entender e modificar
- ✅ Ótimo para APIs REST

### SQLAlchemy
- ✅ Não escrever SQL manualmente
- ✅ Segurança contra SQL injection
- ✅ Código limpo e pythônico
- ✅ Relacionamentos declarativos

### PostgreSQL
- ✅ UUID nativo (melhor que números auto-incremento)
- ✅ Confiável (ACID compliance)
- ✅ Performance
- ✅ Open source

### Docker
- ✅ Reprodutibilidade
- ✅ Fácil onboarding
- ✅ Deploy consistente
- ✅ Isolamento de dependências

---

## Arquitetura da Aplicação

```
┌──────────────────────────────────────────────────────────┐
│                    CLIENTE (Swagger UI)                  │
│              http://localhost:8000/docs                  │
└──────────────────────┬───────────────────────────────────┘
                       │ HTTP Requests
                       ▼
┌──────────────────────────────────────────────────────────┐
│                                                          │
│  FastAPI Application (main.py)                          │
│  ├── /identities → identities.py router               │
│  ├── /applications → applications.py router           │
│  ├── /entitlements → entitlements.py router           │
│  └── /assignments → assignments.py router            │
│                                                          │
└──────────────────┬───────────────────────────────────────┘
                   │ SQLAlchemy ORM
                   ▼
┌──────────────────────────────────────────────────────────┐
│                                                          │
│  Schemas (Pydantic)                                    │
│  ├── identity.py - Valida dados de identity           │
│  ├── applications.py - Valida dados de app             │
│  └── assignments.py - Valida dados de assignment       │
│                                                          │
└──────────────────┬───────────────────────────────────────┘
                   │ SQLAlchemy ORM
                   ▼
┌──────────────────────────────────────────────────────────┐
│                                                          │
│  Models (SQLAlchemy)                                   │
│  ├── identity.py - Classe Identity                    │
│  ├── application.py - Classe Application              │
│  ├── application_entitlement.py - Classe AppEntitle  │
│  └── assignment.py - Classe Assignment               │
│                                                          │
└──────────────────┬───────────────────────────────────────┘
                   │ SQL Queries
                   ▼
┌──────────────────────────────────────────────────────────┐
│                                                          │
│  PostgreSQL Database                                   │
│  ├── identities table                                 │
│  ├── applications table                              │
│  ├── application_entitlements table                  │
│  └── assignments table                              │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## Fluxo de uma Requisição

### Exemplo: POST /identities

```
1. Cliente envia JSON
   {
     "employee_id": "10001",
     "username": "juan",
     "email": "juan@example.com",
     "name": "Juan García",
     "department": "engineering",
     "job_title": "software-engineer"
   }
   ↓
2. FastAPI recebe no routes/identities.py
   ↓
3. Pydantic (schemas/identity.py) valida:
   ✓ Email é válido?
   ✓ Todos os campos obrigatórios?
   ✓ Comprimento correto?
   ↓
4. Se válido, cria modelo SQLAlchemy
   new_identity = Identity(
     employee_id=data.employee_id,
     username=data.username,
     ...
   )
   ↓
5. Verifica se já existe (unique constraints)
   ↓
6. SQLAlchemy gera SQL INSERT
   INSERT INTO identities (employee_id, username, ...)
   VALUES ('10001', 'juan', ...)
   ↓
7. PostgreSQL executa e retorna ID gerado
   ↓
8. FastAPI serializa para JSON e retorna
   {
     "id": "550e8400-e29b-41d4-a716-446655440000",
     "username": "juan",
     "status": "ACTIVE"
   }
```

---

## Estrutura de Pastas

```
blackcat/
├── app/
│   ├── models/                          # Modelos SQLAlchemy
│   │   ├── __init__.py
│   │   ├── identity.py                 # Usuários
│   │   ├── application.py              # Ferramentas
│   │   ├── application_entitlement.py  # Níveis
│   │   └── assignment.py               # Atribuições
│   │
│   ├── schemas/                         # Validação Pydantic
│   │   ├── __init__.py
│   │   ├── identity.py
│   │   ├── applications.py
│   │   └── assignments.py
│   │
│   ├── routes/                          # Endpoints FastAPI
│   │   ├── __init__.py
│   │   ├── identities.py               # POST/GET/PATCH /identities
│   │   ├── applications.py             # POST/GET /applications
│   │   ├── entitlements.py             # POST/GET /entitlements
│   │   └── assignments.py              # POST/GET /assignments
│   │
│   ├── database.py                      # Configuração PostgreSQL
│   └── main.py                          # App principal
│
├── docker/
│   └── Dockerfile                       # Imagem Docker
│
├── docker-compose.yml                   # Orquestração
├── pyproject.toml                       # Dependências
└── README.md                            # Documentação
```

---

## Relacionamentos de Banco

```
┌────────────────┐
│  identities    │
├────────────────┤
│ id (PK)        │
│ employee_id    │
│ username       │
│ email          │
│ name           │
│ department     │
│ job_title      │
│ status         │
│ created_at     │
│ updated_at     │
└────────────────┘
       │
       │ 1-para-N
       │
       ▼
┌────────────────────────┐
│   assignments          │
├────────────────────────┤
│ id (PK)                │
│ identity_id (FK) ──────┼─→ identities.id
│ entitlement_id (FK) ──┐│
│ status                 ││
│ source                 ││
│ created_at             ││
│ expires_at             ││
│ updated_at             ││
└────────────────────────┘
                         │
                         │ N-para-1
                         │
                         ▼
        ┌────────────────────────────────┐
        │ application_entitlements       │
        ├────────────────────────────────┤
        │ id (PK)                        │
        │ application_id (FK) ──────────┐│
        │ name                           ││
        │ description                    ││
        │ created_at                     ││
        │ updated_at                     ││
        └────────────────────────────────┘
                         │
                         │ N-para-1
                         │
                         ▼
        ┌──────────────────────┐
        │   applications       │
        ├──────────────────────┤
        │ id (PK)              │
        │ name                 │
        │ description          │
        │ created_at           │
        │ updated_at           │
        └──────────────────────┘
```

---

## Decisões de Design

### 1. UUIDs vs Auto-increment IDs
**Escolha:** UUID

**Por quê:**
- ✅ Únicos globalmente (não depende do banco)
- ✅ Seguros (não expõem quantidade de registros)
- ✅ Distribuídos (bom para microserviços)
- ✅ PostgreSQL nativo

### 2. Enum vs String para Status/Source
**Escolha:** Enum (tipo SQLEnum)

**Por quê:**
- ✅ Type-safe (não pode enviar valores inválidos)
- ✅ Performance (menos espaço no banco)
- ✅ Integridade de dados
- ✅ PostgreSQL ENUM type

### 3. Soft Delete vs Hard Delete
**Escolha:** Soft Delete (muda status)

**Por quê:**
- ✅ Auditoria (sabe quando foi deletado)
- ✅ Histórico (pode recuperar dados)
- ✅ Relacionamentos (não quebra FK)
- ✅ Compliance (retenção legal)

### 4. Acesso temporário com expires_at
**Escolha:** Campo nullable na tabela

**Por quê:**
- ✅ Simples (campo opcional)
- ✅ Flexível (alguns acessos expiram, outros não)
- ✅ Rastreável (quando expira?)
- ✅ Futuro (fácil adicionar job para expiração automática)

---

## Performance

### Índices

```python
# Identities
- employee_id (UNIQUE)
- username (UNIQUE)
- email (UNIQUE)
- status (filtros frequentes)

# Applications
- name (UNIQUE)

# ApplicationEntitlements
- application_id (ForeignKey)
- name (busca por nome)

# Assignments
- identity_id (ForeignKey)
- entitlement_id (ForeignKey)
- status (filtros frequentes)
- source (filtros frequentes)
```

### Pool de Conexões

```python
# PostgreSQL usa pool de conexões
# Evita criar nova conexão a cada request
pool_pre_ping=True  # Verifica se conexão está viva
```

---

## Segurança

### Validação
```python
# Pydantic valida automaticamente:
- Email válido (EmailStr)
- Comprimento de strings
- Tipos de dados
- Valores enum
```

### SQL Injection Prevention
```python
# SQLAlchemy usa prepared statements automaticamente
# Nunca usar string formatting em queries
```

### Unique Constraints
```python
# Database enforces:
- employee_id único
- username único
- email único
- Impossível duplicar
```

---

## Escalabilidade

### Pronto para crescer

```
Atual:
┌─────────────┐
│ PostgreSQL  │
└─────────────┘

Futuro (quando crescer):
┌──────────────────────────────────┐
│ Read Replicas (leitura)          │
│ ↑                                │
│ Primary PostgreSQL (escrita)     │
└──────────────────────────────────┘

Mais futuro:
┌──────────────────────────────────┐
│ Redis Cache (assignments)        │
│ FastAPI Instances (load balance) │
│ Primary PostgreSQL               │
└──────────────────────────────────┘
```

---

## Deployment

### Local (Development)
```bash
docker-compose up
# FastAPI + PostgreSQL rodando
```

### Produção (Futuro)
```
Kubernetes/Docker Swarm
- FastAPI app (scalable)
- PostgreSQL (managed)
- Redis cache (opcional)
- Monitoring (Prometheus)
- Logging (ELK stack)
```

---

**Última atualização:** 2025-01-15
