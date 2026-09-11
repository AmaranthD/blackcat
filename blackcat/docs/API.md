# 📚 BlackCat API Documentation

Bem-vindo à documentação do BlackCat! Escolha o tópico que deseja aprender:

---

## 📋 Índice Geral

### 🏗️ **Arquitetura & Conceitos**
- [**Arquitetura Geral**](./ARCHITECTURE.md) - Stack, tecnologias, diagrama de fluxo
- [**Conceitos Fundamentais**](./CONCEPTS.md) - IGA vs RBAC, o que é cada coisa

### 👤 **Identities (Usuários)**
- [**Identities Guide**](./IDENTITIES.md) - Tudo sobre usuários, como criar, atualizar, listar
  - Modelo de dados
  - Todos os endpoints
  - Status e regras
  - Exemplos práticos

### 🛠️ **Applications & Entitlements**
- [**Applications Guide**](./APPLICATIONS.md) - Gerenciar aplicações e seus níveis de acesso
  - Criando aplicações
  - Criando entitlements
  - Relacionamentos
  - Exemplos

### 🔐 **Assignments (O Core!)**
- [**Assignments Guide**](./ASSIGNMENTS.md) - Conceder e gerenciar acessos (a parte mais importante!)
  - Como atribuir acessos
  - Source (MANUAL, POLICY, IMPORT)
  - Status e expiração
  - Cenários de uso

### 📊 **Cenários de Uso**
- [**Use Cases**](./USE_CASES.md) - Exemplos reais de fluxos completos
  - Onboarding de novo dev
  - Acesso temporário
  - Auditoria
  - Revogar acessos

### 🔧 **Para Desenvolvedores**
- [**Development Guide**](./DEVELOPMENT.md) - Como adicionar features, testar, deployar

---

## 🚀 Quick Start

### 1. Entender o conceito (2 min)
Leia [Conceitos Fundamentais](./CONCEPTS.md)

### 2. Inicie o Docker
```bash
docker-compose up
```

### 3. Crie seus primeiros dados
1. Crie uma aplicação: [Applications Guide](./APPLICATIONS.md)
2. Crie um entitlement: [Applications Guide](./APPLICATIONS.md)
3. Crie um usuário: [Identities Guide](./IDENTITIES.md)
4. Atribua acesso: [Assignments Guide](./ASSIGNMENTS.md)

### 4. Teste via Swagger
```
http://localhost:8000/docs
```

---

## 📖 Por onde começar?

**Sou um designer/PM e quero entender o conceito:**
→ Leia [Conceitos Fundamentais](./CONCEPTS.md)

**Sou dev e quero integrar identities:**
→ Leia [Identities Guide](./IDENTITIES.md)

**Sou dev e preciso gerenciar aplicações:**
→ Leia [Applications Guide](./APPLICATIONS.md)

**Sou dev e preciso atribuir acessos:**
→ Leia [Assignments Guide](./ASSIGNMENTS.md) ⭐ LEIA ISSO PRIMEIRO!

**Sou admin e preciso fazer um fluxo inteiro:**
→ Leia [Use Cases](./USE_CASES.md)

**Vou adicionar uma nova feature:**
→ Leia [Development Guide](./DEVELOPMENT.md)

---

## Arquitetura

### Stack Tecnológico

```
┌─────────────────────────────────────────────────┐
│         FastAPI (Python Web Framework)          │
├─────────────────────────────────────────────────┤
│              SQLAlchemy ORM                     │
├─────────────────────────────────────────────────┤
│         PostgreSQL (Banco de Dados)             │
├─────────────────────────────────────────────────┤
│        Docker (Containerização)                 │
└─────────────────────────────────────────────────┘
```

**Por quê essas tecnologias?**
- **FastAPI**: Rápida, moderna, com validação automática
- **SQLAlchemy**: ORM poderosa para SQL
- **PostgreSQL**: Banco robusto, suporta UUIDs nativamente
- **Docker**: Deploy consistente em qualquer máquina

---

## Modelos de Dados

### 1. Identity (identities table)

```python
class Identity(Base):
    __tablename__ = "identities"
    
    id: UUID (Primary Key)
    employee_id: String (Unique) - ID do RH
    username: String (Unique) - Login do usuário
    email: String (Unique) - Email corporativo
    name: String - Nome completo
    department: String - Departamento (engineering, sales, hr)
    job_title: String - Cargo (senior-engineer, manager)
    status: Enum - ACTIVE | SUSPENDED | DISABLED
    created_at: DateTime - Quando foi criado
    updated_at: DateTime - Última atualização
```

**Relacionamentos:**
- 1-para-N com **Assignments** (um usuário tem vários acessos)

**Exemplo:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "employee_id": "10001",
  "username": "juan",
  "email": "juan@example.com",
  "name": "Juan García",
  "department": "engineering",
  "job_title": "senior-engineer",
  "status": "ACTIVE",
  "created_at": "2025-01-15T10:30:00",
  "updated_at": "2025-01-15T10:30:00"
}
```

---

### 2. Application (applications table)

```python
class Application(Base):
    __tablename__ = "applications"
    
    id: UUID (Primary Key)
    name: String (Unique) - Nome da aplicação
    description: String - Descrição
    created_at: DateTime
    updated_at: DateTime
```

**Relacionamentos:**
- 1-para-N com **ApplicationEntitlement** (uma app tem vários níveis)

**Exemplo:**
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "name": "GitHub",
  "description": "Repository management platform",
  "created_at": "2025-01-01T00:00:00",
  "updated_at": "2025-01-01T00:00:00"
}
```

---

### 3. ApplicationEntitlement (application_entitlements table)

```python
class ApplicationEntitlement(Base):
    __tablename__ = "application_entitlements"
    
    id: UUID (Primary Key)
    application_id: UUID (Foreign Key) - Link para Application
    name: String - Nome do entitlement (developer, viewer, admin)
    description: String - Descrição
    created_at: DateTime
    updated_at: DateTime
```

**Relacionamentos:**
- N-para-1 com **Application** (muitos entitlements para 1 app)
- 1-para-N com **Assignment** (um entitlement concedido a vários usuários)

**Exemplo:**
```json
{
  "id": "770e8400-e29b-41d4-a716-446655440002",
  "application_id": "660e8400-e29b-41d4-a716-446655440001",
  "name": "developer",
  "description": "Can read and push to repositories",
  "created_at": "2025-01-01T00:00:00",
  "updated_at": "2025-01-01T00:00:00"
}
```

---

### 4. Assignment (assignments table) - O CORE!

```python
class Assignment(Base):
    __tablename__ = "assignments"
    
    id: UUID (Primary Key)
    identity_id: UUID (Foreign Key) - Link para Identity
    entitlement_id: UUID (Foreign Key) - Link para ApplicationEntitlement
    status: Enum - ACTIVE | REVOKED | EXPIRED
    source: Enum - MANUAL | POLICY | IMPORT
    created_at: DateTime - Quando foi criado
    expires_at: DateTime (Nullable) - Quando expira (opcional)
    updated_at: DateTime
```

**Relacionamentos:**
- N-para-1 com **Identity** (um usuário tem muitos assignments)
- N-para-1 com **ApplicationEntitlement** (muitas pessoas têm o mesmo entitlement)

**Enums Importantes:**

**Status:**
- `ACTIVE` - Acesso está ativo agora
- `REVOKED` - Admin revogou manualmente
- `EXPIRED` - Passou da data de expiração

**Source:** ⭐ DIFERENCIA BLACKCAT DO RBAC SIMPLES
- `MANUAL` - Admin concedeu manualmente
- `POLICY` - Regra automática concedeu
- `IMPORT` - Importado de outro sistema (LDAP, AD)

**Exemplo:**
```json
{
  "id": "880e8400-e29b-41d4-a716-446655440003",
  "identity_id": "550e8400-e29b-41d4-a716-446655440000",
  "entitlement_id": "770e8400-e29b-41d4-a716-446655440002",
  "status": "ACTIVE",
  "source": "MANUAL",
  "created_at": "2025-01-15T10:30:00",
  "expires_at": null,
  "updated_at": "2025-01-15T10:30:00"
}
```

---

## APIs e Endpoints

### Identities

#### POST /identities - Criar usuário

**Request:**
```json
{
  "employee_id": "10001",
  "username": "juan",
  "email": "juan@example.com",
  "name": "Juan García",
  "department": "engineering",
  "job_title": "senior-engineer"
}
```

**Response (201 Created):**
```json
{
  "id": "uuid",
  "username": "juan",
  "status": "ACTIVE"
}
```

**Validações:**
- `employee_id`, `username`, `email` devem ser únicos
- Email deve ser válido
- Todos os campos obrigatórios

---

#### GET /identities - Listar usuários

**Query Parameters:**
- `skip`: Pular N usuários (default: 0)
- `limit`: Retornar até N usuários (default: 100)

**Response:**
```json
[
  {
    "id": "uuid",
    "employee_id": "10001",
    "username": "juan",
    "email": "juan@example.com",
    "name": "Juan García",
    "department": "engineering",
    "job_title": "senior-engineer",
    "status": "ACTIVE",
    "created_at": "2025-01-15T10:30:00",
    "updated_at": "2025-01-15T10:30:00"
  }
]
```

---

#### GET /identities/{id} - Obter usuário específico

**Response:**
```json
{
  "id": "uuid",
  "employee_id": "10001",
  "username": "juan",
  "email": "juan@example.com",
  "name": "Juan García",
  "department": "engineering",
  "job_title": "senior-engineer",
  "status": "ACTIVE",
  "created_at": "2025-01-15T10:30:00",
  "updated_at": "2025-01-15T10:30:00"
}
```

---

#### PATCH /identities/{id} - Atualizar usuário

**Request (campos opcionais):**
```json
{
  "name": "Juan García García",
  "job_title": "senior-engineer-2",
  "email": "juan.garcia@example.com"
}
```

**Response:**
```json
{
  "id": "uuid",
  "username": "juan",
  "status": "ACTIVE",
  "updated_at": "2025-01-15T15:45:00"
}
```

---

#### POST /identities/{id}/disable - Desabilitar usuário

**Response:**
```json
{
  "id": "uuid",
  "username": "juan",
  "status": "DISABLED"
}
```

---

### Applications

#### POST /applications - Criar aplicação

**Request:**
```json
{
  "name": "GitHub",
  "description": "Repository management"
}
```

**Response:**
```json
{
  "id": "uuid",
  "name": "GitHub",
  "description": "Repository management",
  "created_at": "2025-01-15T10:30:00",
  "updated_at": "2025-01-15T10:30:00"
}
```

---

#### GET /applications - Listar aplicações

**Response (com entitlements!):**
```json
[
  {
    "id": "app-uuid",
    "name": "GitHub",
    "description": "Repository management",
    "entitlements": [
      {
        "id": "ent-uuid",
        "name": "developer",
        "description": "Can read and push"
      },
      {
        "id": "ent-uuid-2",
        "name": "maintainer",
        "description": "Can merge PRs"
      }
    ],
    "created_at": "2025-01-15T10:30:00"
  }
]
```

---

### Entitlements

#### POST /applications/{app_id}/entitlements - Criar entitlement

**Request:**
```json
{
  "name": "developer",
  "description": "Developer access level"
}
```

**Response:**
```json
{
  "id": "uuid",
  "application_id": "app-uuid",
  "name": "developer",
  "description": "Developer access level",
  "created_at": "2025-01-15T10:30:00"
}
```

---

### Assignments - O CORE!

#### POST /assignments - Conceder acesso

**Request:**
```json
{
  "identity_id": "user-uuid",
  "entitlement_id": "ent-uuid",
  "source": "MANUAL",
  "expires_at": "2025-06-30T23:59:59"  // Opcional
}
```

**Response:**
```json
{
  "id": "uuid",
  "identity_id": "user-uuid",
  "entitlement_id": "ent-uuid",
  "status": "ACTIVE",
  "source": "MANUAL",
  "created_at": "2025-01-15T10:30:00",
  "expires_at": "2025-06-30T23:59:59",
  "updated_at": "2025-01-15T10:30:00"
}
```

---

#### GET /assignments/{identity_id}/entitlements - MAIS IMPORTANTE!

**Query Parameters:**
- `active_only`: true (default) - só mostra assignments ativos

**Response:**
```json
[
  {
    "id": "assignment-uuid",
    "identity": {
      "id": "user-uuid",
      "username": "juan",
      "email": "juan@example.com",
      "name": "Juan García"
    },
    "entitlement": {
      "id": "ent-uuid",
      "name": "developer",
      "description": "Can read and push",
      "application": {
        "id": "app-uuid",
        "name": "GitHub"
      }
    },
    "status": "ACTIVE",
    "source": "MANUAL",
    "created_at": "2025-01-15T10:30:00",
    "expires_at": null
  },
  {
    "id": "assignment-uuid-2",
    "identity": {
      "id": "user-uuid",
      "username": "juan",
      "email": "juan@example.com",
      "name": "Juan García"
    },
    "entitlement": {
      "id": "ent-uuid-2",
      "name": "viewer",
      "description": "Read-only access",
      "application": {
        "id": "app-uuid-2",
        "name": "Grafana"
      }
    },
    "status": "ACTIVE",
    "source": "POLICY",
    "created_at": "2025-01-15T10:30:00",
    "expires_at": "2025-06-30T23:59:59"
  }
]
```

**Use Case:** "Mostrar ao usuário todos os acessos que ele tem"

---

#### POST /assignments/{assignment_id}/revoke - Revogar acesso

**Response:**
```json
{
  "id": "assignment-uuid",
  "status": "REVOKED"
}
```

---

## Cenários de Uso

### Cenário 1: Onboarding de novo dev

```
1. HR cria Juan no sistema
   POST /identities {...}

2. TI cria aplicações necessárias
   POST /applications {"name": "GitHub"}
   POST /applications {"name": "VPN"}

3. TI cria entitlements
   POST /applications/{github-id}/entitlements {"name": "developer"}
   POST /applications/{vpn-id}/entitlements {"name": "user"}

4. TI concede acessos
   POST /assignments {
     "identity_id": "juan-id",
     "entitlement_id": "github-developer-id",
     "source": "MANUAL"
   }
   POST /assignments {
     "identity_id": "juan-id",
     "entitlement_id": "vpn-user-id",
     "source": "MANUAL"
   }

5. Verificar acessos
   GET /assignments/juan-id/entitlements
```

---

### Cenário 2: Acesso temporário para projeto crítico

```
1. Project manager pede acesso a produção por 48 horas
   POST /assignments {
     "identity_id": "juan-id",
     "entitlement_id": "prod-admin-id",
     "source": "MANUAL",
     "expires_at": "2025-01-17T10:30:00"  // Daqui a 2 dias
   }

2. Depois que expira, status muda para EXPIRED
   (Ainda teremos que implementar verificação automática)

3. Verificar quando expira
   GET /assignments/{assignment_id}
```

---

### Cenário 3: Auditoria - "Quem tem acesso a produção?"

```
1. Listar TODOS os assignments
   GET /assignments?entitlement_id=prod-admin-id

Retorna lista com todos que têm acesso à produção!
```

---

## Desenvolvimento

### Estrutura de Arquivos

```
app/
├── models/
│   ├── __init__.py
│   ├── identity.py
│   ├── application.py
│   ├── application_entitlement.py
│   └── assignment.py
├── schemas/
│   ├── __init__.py
│   ├── identity.py
│   ├── applications.py
│   └── assignments.py
├── routes/
│   ├── __init__.py
│   ├── identities.py
│   ├── applications.py
│   ├── entitlements.py
│   └── assignments.py
├── database.py
└── main.py
```

### Como adicionar um novo endpoint

1. Criar schema em `schemas/novo.py`
2. Criar modelo em `models/novo.py`
3. Criar rotas em `routes/novo.py`
4. Incluir router em `main.py`

### Como testar

```bash
# Via Swagger UI
http://localhost:8000/docs

# Via curl
curl -X POST http://localhost:8000/identities \
  -H "Content-Type: application/json" \
  -d '{...}'
```

---

**Última atualização:** 2025-01-15
