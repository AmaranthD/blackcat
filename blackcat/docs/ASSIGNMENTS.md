# 🔐 Assignments (Acessos)

Um **Assignment** é você dando acesso a uma pessoa.

```
Assignment = Decisão de acesso

Juan + GitHub/developer = Assignment
Significa: Juan tem acesso de developer no GitHub
```

---

## Status

| Status | O que é |
|--------|---------|
| **ACTIVE** | Acesso está funcionando agora |
| **REVOKED** | Admin revogou |
| **EXPIRED** | Prazo terminou |

---

## Source - A Origem do Acesso

Isso é importante! Mostra DE ONDE veio o acesso:

| Source | Significado |
|--------|-------------|
| **MANUAL** | Admin deu manualmente |
| **POLICY** | Regra automática deu |
| **IMPORT** | Veio de outro sistema |

---

## Dar Acesso a Uma Pessoa

```bash
POST /assignments

{
  "identity_id": "uuid-do-juan",
  "entitlement_id": "uuid-github-developer",
  "source": "MANUAL",
  "expires_at": "2025-06-30"  # Opcional - para acesso temporário
}
```

---

## Ver Todos os Acessos de Uma Pessoa

```bash
GET /assignments/uuid-do-juan/entitlements
```

Retorna: Lista completa de tudo que Juan pode fazer

---

## Revogar Acesso (Tirar Acesso)

```bash
POST /assignments/uuid-do-assignment/revoke
```

Pronto! Juan perdeu o acesso.

---

## Exemplo Prático

```
1. Cria Juan (Identity)
2. Cria GitHub com entitlement "developer" (Application + Entitlement)
3. Dá acesso de GitHub/developer para Juan (Assignment)
4. Ver: Juan tem GitHub/developer
5. Depois: Revoga o acesso
```

---

**Última atualização:** 2025-01-15
