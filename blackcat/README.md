# OpenIGA

Descrição do seu projeto OpenIGA.

## Estrutura do Projeto

```
openiga/
├── app/              # Código principal da aplicação
├── tests/            # Testes unitários e de integração
├── docker/           # Arquivos Docker
├── docs/             # Documentação
├── examples/         # Exemplos de uso
├── docker-compose.yml
├── pyproject.toml
├── README.md
└── .gitignore
```

## Instalação

### Com pip

```bash
pip install -e .
```

### Com pip (desenvolvimento)

```bash
pip install -e ".[dev]"
```

## Usando Docker Compose

```bash
docker-compose up
```

## Desenvolvendo

### Executando testes

```bash
pytest
```

### Verificando código

```bash
black .
ruff check .
mypy .
```

## Documentação

Consulte a pasta `docs/` para mais informações.

## Exemplos

Exemplos de uso estão disponíveis em `examples/`.

## Licença

MIT
