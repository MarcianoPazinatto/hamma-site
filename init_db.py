"""
Script para inicializar o banco de dados e criar o usuário admin.
Execute apenas uma vez na primeira inicialização do projeto.
Usa variáveis de ambiente para criar o admin em produção.
"""

import os
from sqlalchemy import text, inspect
from app.database import engine, SessionLocal, Base
from app.models import User
from app.auth import get_password_hash


def ensure_cloudinary_columns():
    """Adiciona as colunas cloudinary ao banco de dados se não existirem"""
    print("🔍 Verificando colunas Cloudinary na tabela images...")
    
    try:
        # Inspecionar a tabela images
        inspector = inspect(engine)
        columns = inspector.get_columns('images')
        column_names = [col['name'] for col in columns]
        
        # Verificar quais colunas faltam
        missing_columns = []
        if 'cloudinary_url' not in column_names:
            missing_columns.append('cloudinary_url')
        if 'cloudinary_public_id' not in column_names:
            missing_columns.append('cloudinary_public_id')
        
        if not missing_columns:
            print("  ✅ Colunas Cloudinary já existem!")
            return True
        
        # Adicionar colunas faltando
        print(f"  ⚠️  Colunas faltando: {missing_columns}")
        print(f"  🔧 Adicionando colunas...")
        
        # Usar raw connection para executar ALTER TABLE
        from sqlalchemy.pool import StaticPool
        conn = engine.raw_connection()
        cursor = conn.cursor()
        
        for col in missing_columns:
            try:
                if col == 'cloudinary_url':
                    cursor.execute("ALTER TABLE images ADD COLUMN cloudinary_url VARCHAR(500) DEFAULT NULL")
                elif col == 'cloudinary_public_id':
                    cursor.execute("ALTER TABLE images ADD COLUMN cloudinary_public_id VARCHAR(500) DEFAULT NULL")
                conn.commit()
                print(f"    ✅ Coluna '{col}' adicionada!")
            except Exception as e:
                if "already exists" in str(e) or "duplicate" in str(e):
                    print(f"    ℹ️  Coluna '{col}' já existe!")
                else:
                    print(f"    ⚠️  Erro ao adicionar '{col}': {e}")
        
        cursor.close()
        conn.close()
        
        print("  ✅ Colunas Cloudinary adicionadas com sucesso!")
        return True
        
    except Exception as e:
        print(f"  ❌ Erro ao adicionar colunas Cloudinary: {e}")
        return False


def init_db():
    """Cria as tabelas e o usuário admin"""
    
    # Criar todas as tabelas
    print("📦 Criando tabelas do banco de dados...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tabelas criadas com sucesso!")
    
    # Adicionar colunas Cloudinary se não existirem
    ensure_cloudinary_columns()
    
    # Criar usuário admin
    db = SessionLocal()
    try:
        # Obter credenciais do admin das variáveis de ambiente
        admin_username = os.getenv("ADMIN_USERNAME", "marcianopaz")
        admin_email = os.getenv("ADMIN_EMAIL", "marcianopazinatto@gmail.com")
        admin_password = os.getenv("ADMIN_PASSWORD", "Admin@123")
        
        # Verificar se o admin já existe
        admin = db.query(User).filter(User.username == admin_username).first()
        
        if admin:
            print(f"⚠️  Usuário admin '{admin_username}' já existe. Pulando criação.")
            return
        
        # Criar novo admin
        admin_user = User(
            username=admin_username,
            email=admin_email,
            hashed_password=get_password_hash(admin_password),
            is_active=1,  # Admin já está ativo
            is_admin=1    # É administrador
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print("\n" + "="*50)
        print("✅ USUÁRIO ADMIN CRIADO COM SUCESSO!")
        print("="*50)
        print(f"👤 Username: {admin_username}")
        print(f"📧 Email: {admin_email}")
        print(f"🔐 Senha: {admin_password}")
        print("="*50)
        print("\n⚠️  IMPORTANTE: Mude a senha do admin na primeira vez que fazer login!")
        print("📍 Acesse: http://localhost:8000/login\n")
        
    except Exception as e:
        print(f"❌ Erro ao criar usuário admin: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("\n🚀 Inicializando Hama Sharing App...\n")
    init_db()
    print("✨ Inicialização completa!\n")
