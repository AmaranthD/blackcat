# 🐱 BlackCat - Identity Governance & Administration

Bem-vindo ao **BlackCat**! Um sistema inteligente para gerenciar quem tem acesso a quê na sua empresa.

## O que é BlackCat?

Imagine que você é o gerente de TI de uma empresa. Você precisa responder perguntas como:

- **Quem é Juan?** - Engenheiro de software do departamento de engenharia
- **Quais ferramentas a empresa usa?** - GitHub, Grafana, VPN, Jira, Confluence...
- **Quais níveis de acesso existem?** - developer, viewer, admin, user...
- **Quem tem acesso a quê?** - Juan tem GitHub/developer, Grafana/viewer...
- **Por quanto tempo?** - Para sempre, ou expira em 6 meses?
- **Por que Juan tem esse acesso?** - Um admin deu (MANUAL), uma regra automática deu (POLICY), ou foi importado de outro sistema (IMPORT)?

O **BlackCat** responde todas essas perguntas! 🎯

---

## 🧩 Como funciona? (Bem simples)

### 1. **Identity** - "Quem?"
```
Juan
├── employee_id: "10001"
├── username: "juan"
├── email: "juan@example.com"
├── name: "Juan García"
├── department: "engineering"
├── job_title: "software-engineer"
└── status: "ACTIVE" (ou SUSPENDED, DISABLED)
```
É como um **"cartão de funcionário digital"**. Tem todas as informações de Juan.

---

### 2. **Application** - "Quais ferramentas?"
```
Applications (Ferramentas da empresa)
├── GitHub
├── Grafana
├── VPN
├── Jira
└── Keycloak
```
São os **"sistemas"** que a empresa usa.

---

### 3. **Entitlement** - "Quais níveis?"
```
GitHub tem:
├── developer (pode programar, fazer PR)
├── maintainer (pode revisar código)
└── owner (controla tudo do repo)

Grafana tem:
├── viewer (só vê gráficos)
├── editor (pode criar dashboards)
└── admin (controla tudo)
```
São os **"papéis"** dentro de cada ferramenta.

---

### 4. **Assignment** - "Quem tem acesso a quê?"
```
Juan + GitHub/developer = Assignment
├── status: ACTIVE (ativo agora)
├── source: MANUAL (admin deu)
├── expires_at: null (sem vencimento)
└── created_at: 2025-01-15

Juan + Grafana/viewer = Assignment
├── status: ACTIVE
├── source: POLICY (regra automática deu)
├── expires_at: 2025-06-30 (expira em 6 meses)
└── created_at: 2025-01-15
```
É o **"bilhete"** que diz "Juan tem acesso".

---

## 📊 Fluxograma Completo

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│                      BLACKCAT SYSTEM                            │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Identity (Juan)                                         │  │
│  │  └── employee_id: 10001                                  │  │
│  │      username: juan                                      │  │
│  │      department: engineering                             │  │
│  └──────────────────────────────────────────────────────────┘  │
│         │                                                        │
│         │  (Assignments link Identity com Entitlements)         │
│         │                                                        │
│         ├─────→ ┌────────────────────────────────────────┐     │
│         │       │ Assignment #1                          │     │
│         │       │ Source: MANUAL (Admin deu)             │     │
│         │       │ Status: ACTIVE                         │     │
│         │       └──→ GitHub / developer                  │     │
│         │           └──→ Application: GitHub             │     │
│         │       └────────────────────────────────────────┘     │
│         │                                                        │
│         ├─────→ ┌────────────────────────────────────────┐     │
│         │       │ Assignment #2                          │     │
│         │       │ Source: POLICY (Regra automática)      │     │
│         │       │ Status: ACTIVE                         │     │
│         │       │ Expires: 2025-06-30                    │     │
│         │       └──→ Grafana / viewer                    │     │
│         │           └──→ Application: Grafana            │     │
│         │       └────────────────────────────────────────┘     │
│         │                                                        │
│         └─────→ ┌────────────────────────────────────────┐     │
│                 │ Assignment #3                          │     │
│                 │ Source: IMPORT (Importado de LDAP)     │     │
│                 │ Status: ACTIVE                         │     │
│                 └──→ VPN / user                          │     │
│                     └──→ Application: VPN                │     │
│                 └────────────────────────────────────────┘     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Começando (Quick Start)

### 1. Inicie o Docker
```bash
docker-compose up
```

Isso vai:
- Iniciar a aplicação Python (porta 8000)
- Iniciar o PostgreSQL (porta 5432)
- Criar as tabelas automaticamente

### 2. Veja se está rodando
```bash
curl http://localhost:8000/health
```

Resposta:
```json
{
  "status": "healthy",
  "message": "Service is running"
}
```

### 3. Acesse o Swagger UI (interface visual)
```
http://localhost:8000/docs
```

Lá você pode testar todos os endpoints! 🎉

---

## 🔌 Endpoints Principais

### **Identities** (Criar e gerenciar usuários)

```bash
# Criar um novo usuário
POST /identities
{
  "employee_id": "10001",
  "username": "juan",
  "email": "juan@example.com",
  "name": "Juan García",
  "department": "engineering",
  "job_title": "software-engineer"
}

# Listar todos os usuários
GET /identities

# Obter um usuário específico
GET /identities/{id}

# Atualizar um usuário
PATCH /identities/{id}
{
  "job_title": "senior-engineer"
}

# Desabilitar um usuário
POST /identities/{id}/disable
```

---

### **Applications** (Criar ferramentas)

```bash
# Criar uma aplicação
POST /applications
{
  "name": "GitHub",
  "description": "Repository management"
}

# Listar todas as aplicações (com seus entitlements)
GET /applications

# Ver aplicação específica
GET /applications/{app_id}
```

---

### **Entitlements** (Criar níveis de acesso)

```bash
# Criar um entitlement para uma aplicação
POST /applications/{app_id}/entitlements
{
  "name": "developer",
  "description": "Developer access level"
}

# Listar todos os entitlements
GET /entitlements

# Listar entitlements de uma aplicação
GET /applications/{app_id}/entitlements

# Ver entitlement específico
GET /entitlements/{entitlement_id}
```

---

### **Assignments** (O GRANDE JOGO - conceder acessos!)

```bash
# CONCEITO CENTRAL: Dar acesso a Juan
# "Juan tem acesso a GitHub como developer"

POST /assignments
{
  "identity_id": "uuid-do-juan",
  "entitlement_id": "uuid-do-github-developer",
  "source": "MANUAL"  # ou "POLICY" ou "IMPORT"
}

# Listar todos os assignments
GET /assignments

# Ver TODOS os acessos de um usuário (o mais importante!)
GET /assignments/{identity_id}/entitlements
# Retorna:
# - GitHub / developer (MANUAL)
# - Grafana / viewer (POLICY, expira em 6 meses)
# - VPN / user (IMPORT)

# Revogar um acesso (tirar permissão)
POST /assignments/{assignment_id}/revoke

# Ver um assignment específico
GET /assignments/{assignment_id}
```

---

## 📝 Exemplos de Fluxo Completo

### Cenário 1: Novo desenvolvedor entra na empresa

```bash
# 1. Criar o Juan no sistema
POST /identities
{
  "employee_id": "10001",
  "username": "juan",
  "email": "juan@example.com",
  "name": "Juan García",
  "department": "engineering",
  "job_title": "junior-engineer"
}
# Resposta: id = "abc-123-def"

# 2. Dar acesso a GitHub (manualmente)
POST /assignments
{
  "identity_id": "abc-123-def",
  "entitlement_id": "github-developer-uuid",
  "source": "MANUAL"
}
# Resposta: Assignment criado ✓

# 3. Dar acesso a VPN (via política automática)
# (Será explicado depois quando temos Policy Engine)

# 4. Ver TODOS os acessos de Juan
GET /assignments/abc-123-def/entitlements
# Resposta: Lista de todos os acessos
```

---

### Cenário 2: Juan é promovido para Senior

```bash
# 1. Atualizar o cargo
PATCH /identities/abc-123-def
{
  "job_title": "senior-engineer"
}

# 2. Dar acesso mais alto no GitHub
POST /assignments
{
  "identity_id": "abc-123-def",
  "entitlement_id": "github-maintainer-uuid",
  "source": "MANUAL"
}

# 3. Verificar que ele ainda tem o anterior também
GET /assignments/abc-123-def/entitlements
# Resposta: Agora tem DOIS entitlements GitHub
# - developer (da primeiro)
# - maintainer (novo)
```

---

### Cenário 3: Acesso temporário para um projeto

```bash
# Juan precisa acessar produção por 2 semanas
POST /assignments
{
  "identity_id": "juan-uuid",
  "entitlement_id": "prod-admin-uuid",
  "source": "MANUAL",
  "expires_at": "2025-02-01"  # Daqui a 2 semanas
}

# Sistema automaticamente marca como EXPIRED depois
```

---

## 🎯 IGA vs RBAC Simples

### ❌ RBAC Antigo (Role Based Access Control)
```
Juan tem role "engineer"
→ Pronto, ele tem todos os acessos de engineers
→ Ninguém sabe quando começou, se vai expirar, por que...
→ Impossível auditar
```

### ✅ IGA (Identity Governance & Administration) - BlackCat
```
Juan tem um Assignment para GitHub/developer
✓ Quando começou: 2025-01-15
✓ Por quê: MANUAL (admin João deu)
✓ Até quando: Sem vencimento (null)
✓ Status: ACTIVE
✓ Auditável completamente!

Juan tem um Assignment para Grafana/viewer
✓ Quando começou: 2025-01-15
✓ Por quê: POLICY (regra automática)
✓ Até quando: 2025-06-30 (vai expirar)
✓ Status: ACTIVE (por enquanto)
✓ Histórico completo!
```

---

## 📚 Estrutura de Pastas

```
blackcat/
├── app/
│   ├── models/               # Definições dos dados
│   │   ├── identity.py       # Usuários
│   │   ├── application.py    # Ferramentas
│   │   ├── application_entitlement.py  # Níveis
│   │   └── assignment.py     # Atribuições
│   ├── schemas/              # Validação de dados
│   │   ├── identity.py
│   │   ├── applications.py
│   │   └── assignments.py
│   ├── routes/               # APIs/Endpoints
│   │   ├── identities.py
│   │   ├── applications.py
│   │   ├── entitlements.py
│   │   └── assignments.py
│   ├── main.py              # Aplicação principal
│   └── database.py          # Configuração do PostgreSQL
├── docker-compose.yml        # Configuração do Docker
├── pyproject.toml            # Dependências Python
└── README.md                 # Este arquivo!
```

---

## 🔮 O que vem a seguir?

- [ ] **Policy Engine** - Regras automáticas para dar acessos
- [ ] **Audit Logs** - Histórico completo de mudanças
- [ ] **Access Requests** - Usuários podem pedir acessos
- [ ] **Approval Workflow** - Gerentes aprovam pedidos
- [ ] **Integração com LDAP/AD** - Sincronizar com Active Directory
- [ ] **Webhooks** - Notificar sistemas externos quando acesso muda
- [ ] **Dashboard** - Visualizar acessos em tempo real

---

## 💡 Resumo em 3 Frases

1. **Identity** = Quem é você (Juan)
2. **Application + Entitlement** = Quais ferramentas e níveis existem (GitHub/developer)
3. **Assignment** = Decidir quem tem acesso a quê, por quanto tempo, por quê, e se é manual ou automático

**= Um sistema completo de governança de identidades! 🎉**

---

## 🆘 Dúvidas?

- **Swagger UI**: http://localhost:8000/docs (visualmente mais fácil!)
- **Health Check**: http://localhost:8000/health (testa se está rodando)
- **Root**: http://localhost:8000/ (mensagem de boas-vindas)

---

## 📄 Licença

MIT

---

**Feito com ❤️ para gerenciar acessos de forma inteligente! 🐱**
