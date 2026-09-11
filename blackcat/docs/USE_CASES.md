# 📊 Exemplos de Uso

Fluxos comuns do dia a dia.

---

## Exemplo 1: Novo Dev na Empresa

```
1. Cria usuário Maria (POST /identities)
2. Cria GitHub/developer se não existe (POST /applications e /entitlements)
3. Dá acesso: Maria + GitHub/developer (POST /assignments)
4. Verifica: Maria tem acesso (GET /assignments/maria-uuid/entitlements)
```

---

## Exemplo 2: Consultoria Temporária

```
1. Cria usuário Carlos (POST /identities)
2. Dá acesso com prazo:
   POST /assignments
   {
     "identity_id": "carlos-uuid",
     "entitlement_id": "prod-admin",
     "expires_at": "2025-02-01"  # 2 semanas depois
   }
3. Após 2 semanas: acesso expira automaticamente
```

---

## Exemplo 3: Mudança de Cargo

```
1. Atualiza cargo: PATCH /identities/pedro-uuid {"job_title": "senior"}
2. Dá novo acesso: POST /assignments (GitHub/maintainer)
3. Verifica: GET /assignments/pedro-uuid/entitlements
```

---

## Exemplo 4: Saída de Funcionário

```
1. Desabilita: POST /identities/joao-uuid/disable
2. Revoga tudo:
   - Ver: GET /assignments/joao-uuid/entitlements
   - Para cada acesso: POST /assignments/{id}/revoke
3. Verifica: GET /assignments/joao-uuid/entitlements (vazio)
```

---

## Exemplo 5: Auditoria - Quem tem acesso?

```
# Quem tem GitHub/developer?
GET /assignments?entitlement_id=github-dev-uuid

# Todos os acessos de Juan?
GET /assignments/juan-uuid/entitlements
```

---

**Última atualização:** 2025-01-15
