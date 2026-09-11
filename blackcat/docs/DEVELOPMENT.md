# 🔧 Development

## Setup

```bash
git clone <seu-repo>
cd blackcat
docker-compose up
```

Isso inicia:
- FastAPI na porta 8000
- PostgreSQL na porta 5432
- Tabelas criadas automaticamente

Teste: `curl http://localhost:8000/health`

Swagger UI: `http://localhost:8000/docs`

---

## Estrutura

```
app/
├── models/           # Banco de dados
├── schemas/          # Validação de dados
├── routes/           # Endpoints
├── database.py       # Configuração DB
└── main.py           # App
```

---

## Adicionar Endpoint

**Arquivo:** `app/routes/identities.py`

```python
@router.post("/endpoint-novo")
async def novo_endpoint(data: SeuSchema, db: Session = Depends(get_db)):
    # Seu código aqui
    return {"resultado": "ok"}
```

**Testar:** Via Swagger UI ou curl

---

## Testar

```bash
# Ver logs
docker-compose logs -f app

# Conectar ao banco
docker-compose exec postgres psql -U postgres -d blackcat_db

# Reiniciar tudo
docker-compose down -v
docker-compose up
```

---

**Última atualização:** 2025-01-15
