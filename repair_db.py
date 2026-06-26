"""
Script to repair the database by adding missing Cloudinary columns to the images table.
This script is safe to run multiple times - it checks if columns exist before adding them.
"""

import os
import sys
from sqlalchemy import text, inspect, create_engine
from sqlalchemy.pool import StaticPool
from app.config import get_settings

def check_column_exists(connection, table_name, column_name):
    """Check if a column exists in PostgreSQL using information_schema"""
    try:
        result = connection.execute(
            text("""
                SELECT EXISTS (
                    SELECT 1 FROM information_schema.columns 
                    WHERE table_name = :table AND column_name = :column
                )
            """),
            {"table": table_name, "column": column_name}
        )
        return result.scalar()
    except Exception as e:
        print(f"  ⚠️  Erro ao verificar coluna: {e}")
        return False

def repair_database():
    """Add missing Cloudinary columns to images table if they don't exist"""
    
    print("🔍 Verificando estrutura da tabela 'images'...")
    
    # Get database URL from settings
    settings = get_settings()
    database_url = settings.DATABASE_URL
    
    # Create a new engine connection with explicit transaction handling
    try:
        engine = create_engine(database_url, isolation_level="AUTOCOMMIT")
        connection = engine.connect()
    except Exception as e:
        print(f"❌ Erro ao conectar ao banco de dados: {e}")
        return False
    
    try:
        # Check which columns exist
        print("  → Verificando coluna 'cloudinary_url'...")
        has_cloudinary_url = check_column_exists(connection, 'images', 'cloudinary_url')
        
        print("  → Verificando coluna 'cloudinary_public_id'...")
        has_cloudinary_public_id = check_column_exists(connection, 'images', 'cloudinary_public_id')
        
        if has_cloudinary_url and has_cloudinary_public_id:
            print("\n✅ Todas as colunas Cloudinary já existem!")
            return True
        
        # Add missing columns
        if not has_cloudinary_url:
            print("\n  → Adicionando coluna 'cloudinary_url'...")
            try:
                connection.execute(
                    text("ALTER TABLE images ADD COLUMN cloudinary_url VARCHAR(500) DEFAULT NULL")
                )
                print("    ✅ Coluna 'cloudinary_url' adicionada com sucesso")
            except Exception as e:
                print(f"    ❌ Erro ao adicionar 'cloudinary_url': {e}")
        
        if not has_cloudinary_public_id:
            print("\n  → Adicionando coluna 'cloudinary_public_id'...")
            try:
                connection.execute(
                    text("ALTER TABLE images ADD COLUMN cloudinary_public_id VARCHAR(500) DEFAULT NULL")
                )
                print("    ✅ Coluna 'cloudinary_public_id' adicionada com sucesso")
            except Exception as e:
                print(f"    ❌ Erro ao adicionar 'cloudinary_public_id': {e}")
        
        print("\n✅ Banco de dados reparado com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro geral ao reparar banco de dados: {e}")
        print(f"   Tipo de erro: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        try:
            connection.close()
        except:
            pass


if __name__ == "__main__":
    print("\n🚀 Iniciando reparo do banco de dados...\n")
    success = repair_database()
    print("\n✨ Processo concluído!\n")
    exit(0 if success else 1)
