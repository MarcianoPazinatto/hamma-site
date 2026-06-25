#!/bin/bash
# Script de build para Render.com

set -e

echo "🔧 Instalando dependências..."
pip install -r requirements.txt

echo "📦 Inicializando banco de dados..."
python init_db.py

echo "✅ Build completado com sucesso!"
