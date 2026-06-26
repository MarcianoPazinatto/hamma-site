#!/usr/bin/env python
"""
Direct database schema fix using psycopg2.
This script adds missing Cloudinary columns to the images table.
It's more robust than Alembic for emergency fixes.
"""

import os
import sys

def fix_database_schema():
    """Add missing columns directly using psycopg2"""
    
    # Get database URL
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        from app.config import get_settings
        database_url = get_settings().DATABASE_URL
    
    print("🔧 Tentando usar psycopg2 para reparo direto...")
    
    try:
        import psycopg2
        from psycopg2 import sql
        
        # Parse database URL (format: postgresql://user:password@host:port/dbname)
        from urllib.parse import urlparse
        
        parsed = urlparse(database_url)
        
        # Handle different PostgreSQL URL formats
        if 'postgresql+psycopg2' in database_url:
            database_url = database_url.replace('postgresql+psycopg2://', 'postgresql://')
        elif 'postgresql://' not in database_url:
            print("❌ URL de banco de dados não é PostgreSQL")
            return False
        
        # Connect directly
        print(f"  → Conectando ao banco de dados...")
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # Check if columns exist
        print("  → Verificando estrutura da tabela...")
        cursor.execute("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name = 'images'
        """)
        
        existing_columns = [row[0] for row in cursor.fetchall()]
        print(f"    Colunas existentes: {existing_columns}")
        
        # Add missing columns
        columns_to_add = {
            'cloudinary_url': 'VARCHAR(500)',
            'cloudinary_public_id': 'VARCHAR(500)'
        }
        
        for col_name, col_type in columns_to_add.items():
            if col_name not in existing_columns:
                print(f"  → Adicionando coluna '{col_name}'...")
                try:
                    cursor.execute(f"ALTER TABLE images ADD COLUMN {col_name} {col_type} DEFAULT NULL")
                    print(f"    ✅ Coluna '{col_name}' adicionada")
                except psycopg2.Error as e:
                    if "already exists" in str(e):
                        print(f"    ⚠️  Coluna '{col_name}' já existe")
                    else:
                        print(f"    ❌ Erro: {e}")
            else:
                print(f"    ✅ Coluna '{col_name}' já existe")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("\n✅ Banco de dados reparado com sucesso (psycopg2)!")
        return True
        
    except ImportError:
        print("  ⚠️  psycopg2 não disponível, usando SQLAlchemy...")
        return use_sqlalchemy_fix()
    except Exception as e:
        print(f"  ❌ Erro com psycopg2: {e}")
        print("  ⚠️  Tentando com SQLAlchemy...")
        return use_sqlalchemy_fix()


def use_sqlalchemy_fix():
    """Fallback to SQLAlchemy-based fix"""
    
    try:
        from sqlalchemy import create_engine, text
        from app.config import get_settings
        
        settings = get_settings()
        
        # Create engine with AUTOCOMMIT isolation level
        engine = create_engine(
            settings.DATABASE_URL,
            isolation_level="AUTOCOMMIT",
            echo=False
        )
        
        print("  → Conectando com SQLAlchemy...")
        
        with engine.connect() as conn:
            # Check existing columns
            result = conn.execute(text("""
                SELECT column_name FROM information_schema.columns 
                WHERE table_name = 'images'
                ORDER BY column_name
            """))
            
            existing_columns = [row[0] for row in result]
            print(f"    Colunas existentes: {existing_columns}")
            
            # Add missing columns
            if 'cloudinary_url' not in existing_columns:
                print("  → Adicionando coluna 'cloudinary_url'...")
                conn.execute(text("""
                    ALTER TABLE images 
                    ADD COLUMN cloudinary_url VARCHAR(500) DEFAULT NULL
                """))
                print("    ✅ Coluna 'cloudinary_url' adicionada")
            else:
                print("    ✅ Coluna 'cloudinary_url' já existe")
            
            if 'cloudinary_public_id' not in existing_columns:
                print("  → Adicionando coluna 'cloudinary_public_id'...")
                conn.execute(text("""
                    ALTER TABLE images 
                    ADD COLUMN cloudinary_public_id VARCHAR(500) DEFAULT NULL
                """))
                print("    ✅ Coluna 'cloudinary_public_id' adicionada")
            else:
                print("    ✅ Coluna 'cloudinary_public_id' já existe")
        
        print("\n✅ Banco de dados reparado com sucesso (SQLAlchemy)!")
        return True
        
    except Exception as e:
        print(f"  ❌ Erro com SQLAlchemy: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n🚀 Iniciando reparo de schema do banco de dados...\n")
    
    try:
        success = fix_database_schema()
        print(f"\n✨ Processo concluído!\n")
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
