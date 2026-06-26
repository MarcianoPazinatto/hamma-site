#!/bin/bash
# Script de build para Render.com

set -e

echo "🔧 Instalando dependências..."
pip install -r requirements.txt

echo "🗄️ Executando migrations..."
alembic upgrade head

echo "🔧 Reparando banco de dados (adicionando colunas faltando)..."
python repair_db.py

echo "📦 Inicializando banco de dados..."
python init_db.py

echo "✅ Build completado com sucesso!"
