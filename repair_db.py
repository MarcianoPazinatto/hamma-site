"""
Script to repair the database by adding missing Cloudinary columns to the images table.
This script is safe to run multiple times - it checks if columns exist before adding them.
"""

import os
from sqlalchemy import text, inspect
from app.database import engine, SessionLocal
from app.config import get_settings

def repair_database():
    """Add missing Cloudinary columns to images table if they don't exist"""
    
    print("🔍 Verificando estrutura da tabela 'images'...")
    
    # Get database inspector
    inspector = inspect(engine)
    
    # Get columns from images table
    try:
        columns = inspector.get_columns('images')
        column_names = [col['name'] for col in columns]
    except Exception as e:
        print(f"❌ Erro ao inspecionar tabela: {e}")
        return False
    
    print(f"✅ Colunas encontradas: {column_names}")
    
    # Check which columns are missing
    missing_columns = []
    if 'cloudinary_url' not in column_names:
        missing_columns.append('cloudinary_url')
    if 'cloudinary_public_id' not in column_names:
        missing_columns.append('cloudinary_public_id')
    
    if not missing_columns:
        print("✅ Todas as colunas Cloudinary já existem!")
        return True
    
    print(f"⚠️  Colunas faltando: {missing_columns}")
    print("🔧 Adicionando colunas faltando...")
    
    # Add missing columns
    try:
        with engine.connect() as connection:
            if 'cloudinary_url' in missing_columns:
                print("  → Adicionando coluna 'cloudinary_url'...")
                connection.execute(
                    text("ALTER TABLE images ADD COLUMN cloudinary_url VARCHAR(500) NULL")
                )
                connection.commit()
                print("    ✅ Coluna 'cloudinary_url' adicionada")
            
            if 'cloudinary_public_id' in missing_columns:
                print("  → Adicionando coluna 'cloudinary_public_id'...")
                connection.execute(
                    text("ALTER TABLE images ADD COLUMN cloudinary_public_id VARCHAR(500) NULL")
                )
                connection.commit()
                print("    ✅ Coluna 'cloudinary_public_id' adicionada")
        
        print("\n✅ Banco de dados reparado com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao adicionar colunas: {e}")
        print(f"   Tipo de erro: {type(e).__name__}")
        return False

if __name__ == "__main__":
    print("\n🚀 Iniciando reparo do banco de dados...\n")
    success = repair_database()
    print("\n✨ Processo concluído!\n")
    exit(0 if success else 1)
