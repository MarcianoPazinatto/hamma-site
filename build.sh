#!/bin/bash
# Script de build para Render.com

set -e

echo "🔧 Instalando dependências..."
pip install -r requirements.txt

echo "🗄️ Executando migrations..."
alembic upgrade head || echo "⚠️  Alembic upgrade falhou, continuando com fix_schema..."

echo "🔧 Reparando banco de dados (adicionando colunas faltando)..."
python fix_schema.py || python repair_db.py || echo "⚠️  Reparo de schema falhou, continuando..."

echo "📦 Inicializando banco de dados..."
python init_db.py

echo "✅ Build completado com sucesso!"
