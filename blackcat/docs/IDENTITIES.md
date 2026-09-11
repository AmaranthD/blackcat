# 👤 Identities (Usuários)

Uma **Identity** é o perfil de um funcionário no sistema.

```
Identity = Dados do funcionário
Exemplo: Nome, email, cargo, departamento
```

---

## Informações que Guardamos

```
✓ Nome completo
✓ Email corporativo
✓ Login (username)
✓ ID do RH
✓ Cargo
✓ Departamento
✓ Status (ativo, suspenso, desabilitado)
```

---

## Status Simples

| Status | Significado |
|--------|-------------|
| **ACTIVE** | Funcionário ativo, pode ter acessos |
| **SUSPENDED** | Temporariamente sem acesso (licença, férias) |
| **DISABLED** | Saiu da empresa ou foi demitido |

---

## Criar Usuário

```bash
POST /identities

{
  "employee_id": "10001",
  "username": "juan",
  "email": "juan@example.com",
  "name": "Juan García",
  "department": "engineering",
  "job_title": "developer"
}
```

**Retorna:**
```json
{
  "id": "uuid-do-juan",
  "username": "juan",
  "status": "ACTIVE"
}
```

---

## Ver Usuário

```bash
# Ver um
GET /identities/uuid-do-juan

# Ver todos
GET /identities
```

---

## Atualizar Usuário

```bash
PATCH /identities/uuid-do-juan

{
  "job_title": "senior-developer",
  "email": "juan.novo@example.com"
}
```

---

## Desabilitar Usuário

```bash
POST /identities/uuid-do-juan/disable
```

Pronto! Agora o usuário não pode mais acessar nada.

---

## Próximo Passo

Após criar um usuário, você precisa **dar acessos** a ele.

Veja [Assignments](./ASSIGNMENTS.md) para aprender como dar acesso a aplicações!

---

**Última atualização:** 2025-01-15
