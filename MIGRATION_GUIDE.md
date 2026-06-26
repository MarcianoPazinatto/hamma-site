# 📦 Guia de Migration - Atualizar Banco de Dados

Este guia explica como executar a migration para adicionar as colunas do Cloudinary ao banco de dados.

## 🔴 Problema Encontrado

Ao fazer deploy da integração Cloudinary, o banco de dados em produção (PostgreSQL) ainda tem a estrutura antiga. As colunas `cloudinary_url` e `cloudinary_public_id` não existem na tabela `images`.

**Erro**: `sqlalchemy.exc.ProgrammingError: column images.cloudinary_url does not exist`

## ✅ Solução: Usar Alembic para Migration

Criei uma migration com **Alembic** que adiciona as novas colunas de forma segura e permite reverter se necessário.

### Arquivos Criados

- `alembic/` - Diretório com configuração Alembic
- `alembic/env.py` - Configuração do ambiente
- `alembic/script.py.mako` - Template para novas migrations
- `alembic/versions/001_add_cloudinary_columns.py` - Migration que adiciona as colunas
- `alembic.ini` - Arquivo de configuração principal

## 🚀 Como Executar a Migration

### Local (Desenvolvimento)

```bash
# 1. Instale as dependências (se não fez ainda)
pip install -r requirements.txt

# 2. Execute a migration
alembic upgrade head
```

Você deve ver uma saída similar a:
```
INFO  [alembic.runtime.migration] Context impl PostgreSQLImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 001, add cloudinary columns to images table
```

### Em Produção (Render)

#### Opção 1: Via Build Script (Recomendado)

Edite o arquivo `build.sh` para executar a migration:

```bash
#!/usr/bin/env bash
set -e

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running migrations..."
alembic upgrade head

echo "Build completed!"
```

#### Opção 2: Manualmente no Render

1. Acesse o painel do Render
2. Vá para **Settings** do seu serviço
3. Em **Build Command**, adicione:
   ```bash
   pip install -r requirements.txt && alembic upgrade head
   ```
4. Faça deploy novamente

#### Opção 3: Via Render Shell

1. Acesse o painel do Render
2. Clique em **Shell** (se disponível)
3. Execute:
   ```bash
   alembic upgrade head
   ```

## 📋 O Que A Migration Faz

A migration `001_add_cloudinary_columns.py` executa:

1. **Adiciona coluna `cloudinary_url`**: URL pública da imagem no Cloudinary
2. **Adiciona coluna `cloudinary_public_id`**: ID para deletar a imagem do Cloudinary
3. **Torna `filename` nullable**: Para compatibilidade com imagens antigas

## 🔄 Reverter A Migration (Se Necessário)

Se algo der errado, você pode reverter:

```bash
# Reverter última migration
alembic downgrade -1
```

## ✨ Próximas Steps

1. **Executar a migration** (veja instruções acima)
2. **Fazer novo deploy** do projeto
3. **Testar upload de imagem**:
   - Acesse a aplicação
   - Faça login
   - Faça upload de uma imagem
   - A imagem deve ir para o Cloudinary
4. **Verificar no Cloudinary**:
   - Acesse https://cloudinary.com/console/media_library
   - Procure pela pasta "hama-sharing"
   - Imagens devem aparecer lá

## 🧪 Verificar Status da Migration

Para ver quais migrations foram aplicadas:

```bash
# Ver histórico de migrations
alembic history

# Ver versão atual do banco
alembic current
```

## 📝 Criar Nova Migration

Se precisar fazer mais alterações no banco de dados no futuro:

```bash
# Criar nova migration automática (detecta mudanças no modelo)
alembic revision --autogenerate -m "Descrição das mudanças"

# Ou criar migration vazia
alembic revision -m "Descrição das mudanças"
```

Isso criará um novo arquivo em `alembic/versions/` que você pode editar.

## 🆘 Troubleshooting

### "No such table: alembic_version"

Significa que é a primeira vez rodando migration. Isso é normal, o Alembic criará a tabela automaticamente.

### "Column already exists"

Se a coluna já existe, significa que a migration já foi aplicada. Você pode verificar:

```bash
alembic current
```

### Erro ao conectar ao banco

Verifique se `DATABASE_URL` está configurado corretamente:

```bash
# Local (SQLite)
DATABASE_URL=sqlite:///./app.db

# PostgreSQL (Render)
DATABASE_URL=postgresql://user:password@host/dbname
```

## 📚 Referências

- [Documentação Alembic](https://alembic.sqlalchemy.org/)
- [SQLAlchemy Migrations](https://docs.sqlalchemy.org/en/20/orm/dataclasses.html)

---

**Importante**: Execute a migration ANTES de fazer novo deploy com o código da integração Cloudinary. Caso contrário, a aplicação não conseguirá conectar ao banco.


