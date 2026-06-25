"""
Script para inicializar o banco de dados e criar o usuário admin.
Execute apenas uma vez na primeira inicialização do projeto.
Usa variáveis de ambiente para criar o admin em produção.
"""

import os
from app.database import engine, SessionLocal, Base
from app.models import User
from app.auth import get_password_hash


def init_db():
    """Cria as tabelas e o usuário admin"""
    
    # Criar todas as tabelas
    print("📦 Criando tabelas do banco de dados...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tabelas criadas com sucesso!")
    
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
