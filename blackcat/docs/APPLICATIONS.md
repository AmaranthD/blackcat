# 🛠️ Applications & Entitlements

Uma **Application** é uma ferramenta que a empresa usa.

Um **Entitlement** é um nível de acesso dentro daquela ferramenta.

```
Application = Ferramenta (GitHub, Grafana, VPN)
  ├── developer (entitlement)
  ├── maintainer (entitlement)
  └── admin (entitlement)
```

---

## Criar Application

```bash
POST /applications

{
  "name": "GitHub",
  "description": "Repository management"
}
```

---

## Ver Applications

```bash
# Ver todos
GET /applications

# Ver uma específica
GET /applications/uuid-github
```

---

## Criar Entitlement

```bash
POST /applications/uuid-github/entitlements

{
  "name": "developer",
  "description": "Can read and push"
}
```

---

## Ver Entitlements

```bash
# Ver todos de uma app
GET /applications/uuid-github/entitlements

# Ver um específico
GET /entitlements/uuid-do-entitlement
```

---

## Próximo Passo

Após criar Applications e Entitlements, você precisa **dar acessos** a usuários.

Veja [Assignments](./ASSIGNMENTS.md)!

---

**Última atualização:** 2025-01-15
