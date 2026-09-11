# 💡 BlackCat Concepts

Entenda os conceitos principais do BlackCat de forma leiga.

---

## IGA vs RBAC

Essa é a grande diferença do BlackCat!

### ❌ RBAC Simples (Role Based Access Control)

Imagine que você é um admin em uma empresa antiga:

```
System: "Juan tem role 'engineer'"
Admin:  "Ok, ele tem acesso a tudo que engineers têm"
                          
Mas:
- Quando começou? ❌ Ninguém sabe
- Por quanto tempo? ❌ Ninguém sabe
- Por quê? ❌ Ninguém sabe
- Quem deu? ❌ Ninguém sabe
```

**É como dar uma chave de carro:**
```
Admin: "Aqui está a chave do carro da empresa"
Juan: "Obrigado"
... 1 ano depois
Admin: "Juan ainda tem essa chave? Quando começou a usar?"
Admin: "Não sei... 😅"
```

---

### ✅ IGA (Identity Governance & Administration)

Agora com BlackCat:

```
Assignment: Juan + GitHub/developer
├── Quando começou? 2025-01-15 10:30 ✓
├── Por quanto tempo? Até 2025-12-31 ✓
├── Por quê? MANUAL (João admin deu) ✓
├── Quem deu? João (admin) ✓
└── Pode revogar? Sim ✓

Assignment: Juan + Grafana/viewer
├── Quando começou? 2025-01-15 10:30 ✓
├── Por quanto tempo? Até 2025-06-30 ✓
├── Por quê? POLICY (regra automática) ✓
├── Quem deu? Sistema (regra) ✓
└── Pode revogar? Sim ✓
```

**É como alugar um carro:**
```
Contrato:
- Carro: Toyota Corolla
- Quem pega: Juan
- Quando: 15/01/2025
- Até quando: 15/02/2025 (30 dias)
- Por quê: Projeto X (necessário mesmo)
- Assinado por: João (gerente)

Tudo rastreado! ✓
```

---

## A Hierarquia do BlackCat

```
Application (A ferramenta)
    └── GitHub
        
    Entitlements (Os níveis dentro da ferramenta)
        ├── developer (pode programar)
        ├── maintainer (pode revisar)
        └── owner (controla tudo)

Identity (A pessoa)
    └── Juan
        
    Assignments (O que Juan tem)
        └── GitHub / developer
            ├── Status: ACTIVE
            ├── Source: MANUAL
            └── Expires: nunca
```

### Analogia com Restaurante

```
Application = Restaurante "Pizzaria da Mão"

Entitlements = Cargos
├── Gerente (acesso ao caixa, folha de pagamento)
├── Cozinheiro (acesso à cozinha)
├── Garçom (acesso ao salão)
└── Faxineiro (acesso ao depósito)

Identity = Pessoa
├── Juan (gerente)
├── Maria (cozinheira)
└── Pedro (garçom)

Assignment = Atribuição
├── Juan tem cargo "gerente" (source: MANUAL, 2020-01-01)
├── Maria tem cargo "cozinheira" (source: MANUAL, 2021-05-15)
└── Pedro tem cargo "garçom" (source: POLICY, expira em 2025-02-15)
```

---

## Os 4 Pilares

### 1. **Identity** - Quem?

```json
{
  "id": "uuid",
  "employee_id": "10001",
  "username": "juan",
  "email": "juan@example.com",
  "name": "Juan García",
  "department": "engineering",
  "job_title": "software-engineer",
  "status": "ACTIVE"
}
```

**É tipo um CPF/RG:**
- Identifica a pessoa
- Tem informações dela
- Pode estar ativa ou desativa

---

### 2. **Application** - Quais ferramentas?

```json
{
  "id": "uuid",
  "name": "GitHub",
  "description": "Repository management"
}
```

**É tipo um SERVIÇO:**
- GitHub (repositórios)
- Grafana (gráficos)
- VPN (conexão remota)
- Jira (tarefas)

---

### 3. **Entitlement** - Quais níveis?

```json
{
  "id": "uuid",
  "application_id": "github-uuid",
  "name": "developer",
  "description": "Can read and push to repositories"
}
```

**É tipo um CARGO/PERMISSÃO:**
- GitHub tem: developer, maintainer, owner
- Grafana tem: viewer, editor, admin
- VPN tem: user, admin

---

### 4. **Assignment** - Decisão!

```json
{
  "id": "uuid",
  "identity_id": "juan-uuid",
  "entitlement_id": "github-developer-uuid",
  "status": "ACTIVE",
  "source": "MANUAL",
  "created_at": "2025-01-15T10:30:00",
  "expires_at": null
}
```

**É tipo um CONTRATO:**
- Quem? Juan
- O quê? GitHub/developer
- Quando começou? 2025-01-15
- Quando termina? Nunca
- Por quê? Porque alguém (MANUAL) decidiu
- Pode ser revogado? Sim

---

## Source (A Origem do Acesso)

Isso é OURO do BlackCat! Saber POR QUÊ alguém tem acesso.

### MANUAL - "Um admin deu"

```json
{
  "source": "MANUAL",
  "story": "Em 2025-01-15, João (admin) concedeu GitHub/developer a Juan"
}
```

**Cenários:**
- Admin criou assignment manualmente
- Gerente pediu para o admin dar
- Onboarding de novo dev

---

### POLICY - "Uma regra automática deu"

```json
{
  "source": "POLICY",
  "rule": "IF department = 'engineering' THEN grant GitHub/developer"
}
```

**Cenários:**
- Todos de engineering recebem GitHub/developer automaticamente
- Novo dev criado em engineering → automáticamente recebe acesso
- Ninguém precisa fazer nada

---

### IMPORT - "Veio de outro sistema"

```json
{
  "source": "IMPORT",
  "system": "LDAP/Active Directory"
}
```

**Cenários:**
- Sincronizar usuários do AD
- Importar grupos do LDAP
- Migrar de outro sistema IGA

---

## Status (O Estado do Assignment)

### ACTIVE - Ativo agora

```
✓ Juan pode acessar GitHub/developer AGORA
```

### REVOKED - Revogado (admin tirou)

```
✗ Juan NÃO pode mais acessar GitHub/developer
✗ Porque admin revogou manualmente
```

**Cenários:**
- Juan saiu da empresa
- Juan foi transferido de departamento
- Juan fez algo errado
- Projeto terminou

### EXPIRED - Expirado (tempo passou)

```
✗ Juan NÃO pode mais acessar GitHub/developer
✗ Porque o acesso temporário expirou (data de expiração passou)
```

**Cenários:**
- Acesso temporário para projeto de 2 semanas terminou
- Acesso de consultante temporário expirou
- Acesso de estagiário terminou

---

## Expires_at (Acesso Temporário)

Você pode dar acesso com prazo de validade!

```json
{
  "identity_id": "juan-uuid",
  "entitlement_id": "prod-admin-uuid",
  "source": "MANUAL",
  "expires_at": "2025-02-15T23:59:59"  // Válido por 30 dias
}
```

**Benéficos:**
- Segurança (acesso automático removido)
- Conformidade (compliance automatizado)
- Controle (não precisa lembrar de revogar)
- Auditoria (rastreia expiração)

---

## Fluxo Completo (Exemplo Real)

### Juan entra na empresa

```
1. HR cria Identity para Juan
   POST /identities
   {
     "employee_id": "10001",
     "username": "juan",
     "email": "juan@example.com",
     "name": "Juan García",
     "department": "engineering",
     "job_title": "junior-engineer"
   }
   → Identity ID = "abc123"

2. TI procura Entitlements para engineering
   GET /applications/github/entitlements
   → Encontra "developer" ID = "def456"

3. Admin cria Assignment (MANUAL)
   POST /assignments
   {
     "identity_id": "abc123",
     "entitlement_id": "def456",
     "source": "MANUAL"
   }
   → Assignment criado ✓

4. Sistema detecta que department = "engineering"
   → Executa política automática (POLICY)
   POST /assignments
   {
     "identity_id": "abc123",
     "entitlement_id": "grafana-viewer-uuid",
     "source": "POLICY",
     "expires_at": "2025-12-31"
   }
   → Acesso temporário ✓

5. Depois, podemos verificar todos os acessos de Juan
   GET /assignments/abc123/entitlements
   
   Retorna:
   [
     {
       "application": "GitHub",
       "entitlement": "developer",
       "source": "MANUAL",
       "expires_at": null
     },
     {
       "application": "Grafana",
       "entitlement": "viewer",
       "source": "POLICY",
       "expires_at": "2025-12-31"
     }
   ]
```

---

## Por que BlackCat é legal?

| Aspecto | RBAC Antigo | BlackCat IGA |
|---------|------------|------------|
| **Sabe por quê?** | ❌ | ✅ MANUAL/POLICY/IMPORT |
| **Rastreia quando começou?** | ❌ | ✅ created_at |
| **Rastreia quem deu?** | ❌ | ✅ source |
| **Acesso temporário?** | ❌ | ✅ expires_at |
| **Revoga automaticamente?** | ❌ | ✅ (vai implementar) |
| **Auditoria completa?** | ❌ | ✅ (vai implementar) |
| **Cumple GDPR/SOC2?** | ❌ | ✅ |
| **Políticas automáticas?** | ❌ | ✅ (POLICY source) |

---

## Próximos Passos

Depois de entender isso, leia:

1. [**IDENTITIES.md**](./IDENTITIES.md) - Como trabalhar com usuários
2. [**APPLICATIONS.md**](./APPLICATIONS.md) - Como criar apps e entitlements
3. [**ASSIGNMENTS.md**](./ASSIGNMENTS.md) - Como dar acessos ⭐ IMPORTANTE
4. [**USE_CASES.md**](./USE_CASES.md) - Exemplos reais

---

**Última atualização:** 2025-01-15
