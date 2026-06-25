from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from ..database import get_db
from ..models import User
from ..schemas import UserCreate, Token, UserResponse
from ..auth import (
    verify_password,
    get_password_hash,
    create_access_token,
    decode_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """Registra um novo usuário"""
    # Verificar se o usuário já existe
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email já registrado")
    
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username já existe")

    # Criar novo usuário
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/login", response_model=Token)
def login(username: str, password: str, db: Session = Depends(get_db)):
    """Faz login do usuário e retorna um token JWT"""
    # Buscar usuário
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username ou password incorretos",
        )

    # Verificar se o usuário está ativo (aprovado)
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sua conta ainda não foi aprovada. Aguarde a aprovação do administrador.",
        )

    # Criar token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_admin_user(username: str = None, db: Session = None) -> User:
    """Verifica se o usuário é admin"""
    if username is None:
        return None
    
    user = db.query(User).filter(User.username == username).first()
    if not user or not user.is_admin:
        return None
    return user


@router.get("/admin/pending-users")
def get_pending_users(token: str = None, db: Session = Depends(get_db)):
    """Lista usuários pendentes de aprovação (REQUER ADMIN)"""
    if not token:
        raise HTTPException(status_code=401, detail="Token não fornecido")
    
    username = decode_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    admin = get_current_admin_user(username, db)
    if not admin:
        raise HTTPException(status_code=403, detail="Você não tem permissão para acessar este recurso")
    
    users = db.query(User).filter(User.is_active == 0).all()
    return users


@router.post("/admin/approve-user/{user_id}")
def approve_user(user_id: int, token: str = None, db: Session = Depends(get_db)):
    """Aprova um usuário (REQUER ADMIN)"""
    if not token:
        raise HTTPException(status_code=401, detail="Token não fornecido")
    
    username = decode_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    admin = get_current_admin_user(username, db)
    if not admin:
        raise HTTPException(status_code=403, detail="Você não tem permissão para acessar este recurso")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    if user.is_active:
        raise HTTPException(status_code=400, detail="Usuário já foi aprovado")
    
    user.is_active = 1
    db.commit()
    return {"message": f"Usuário {user.username} foi aprovado com sucesso!"}


@router.post("/admin/reject-user/{user_id}")
def reject_user(user_id: int, token: str = None, db: Session = Depends(get_db)):
    """Rejeita um usuário (REQUER ADMIN)"""
    if not token:
        raise HTTPException(status_code=401, detail="Token não fornecido")
    
    username = decode_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    admin = get_current_admin_user(username, db)
    if not admin:
        raise HTTPException(status_code=403, detail="Você não tem permissão para acessar este recurso")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Deletar usuário
    db.delete(user)
    db.commit()
    return {"message": f"Usuário {user.username} foi rejeitado e deletado do sistema!"}


@router.get("/admin/all-users")
def get_all_users(token: str = None, db: Session = Depends(get_db)):
    """Lista todos os usuários (REQUER ADMIN)"""
    if not token:
        raise HTTPException(status_code=401, detail="Token não fornecido")
    
    username = decode_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    admin = get_current_admin_user(username, db)
    if not admin:
        raise HTTPException(status_code=403, detail="Você não tem permissão para acessar este recurso")
    
    users = db.query(User).all()
    return users


@router.get("/user-info")
def get_user_info(token: str = None, db: Session = Depends(get_db)):
    """Retorna informações do usuário logado"""
    if not token:
        return {"authenticated": False, "is_admin": False}
    
    username = decode_token(token)
    if not username:
        return {"authenticated": False, "is_admin": False}
    
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return {"authenticated": False, "is_admin": False}
    
    return {
        "authenticated": True,
        "is_admin": bool(user.is_admin),
        "username": user.username,
        "email": user.email
    }


@router.post("/change-password")
def change_password(old_password: str, new_password: str, token: str = None, db: Session = Depends(get_db)):
    """Muda a senha do usuário logado (REQUER LOGIN)"""
    if not token:
        raise HTTPException(status_code=401, detail="Token não fornecido")
    
    username = decode_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Verificar se a senha antiga está correta
    if not verify_password(old_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Senha antiga incorreta")
    
    # Validar nova senha
    if len(new_password) < 6:
        raise HTTPException(status_code=400, detail="Nova senha deve ter pelo menos 6 caracteres")
    
    if old_password == new_password:
        raise HTTPException(status_code=400, detail="Nova senha não pode ser igual à senha antiga")
    
    # Atualizar senha
    user.hashed_password = get_password_hash(new_password)
    db.commit()
    
    return {"message": "Senha alterada com sucesso!"}


@router.get("/available-urls")
def get_available_urls(token: str = None, db: Session = Depends(get_db)):
    """Retorna as URLs disponíveis para o usuário logado"""
    # URLs públicas (disponíveis para todos)
    public_urls = {
        "GET /": "Homepage com galeria pública",
        "GET /login": "Página de login",
        "GET /register": "Página de registro",
        "GET /images/": "API - Lista todas as imagens"
    }
    
    # URLs para usuários não autenticados
    urls = dict(public_urls)
    
    if not token:
        return {
            "authenticated": False,
            "user_type": "anonymous",
            "available_urls": urls,
            "message": "Faça login para acessar mais funcionalidades"
        }
    
    username = decode_token(token)
    if not username:
        return {
            "authenticated": False,
            "user_type": "anonymous",
            "available_urls": urls
        }
    
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return {
            "authenticated": False,
            "user_type": "anonymous",
            "available_urls": urls
        }
    
    # URLs para usuários logados
    user_urls = dict(public_urls)
    user_urls.update({
        "GET /dashboard": "Painel do usuário para gerenciar imagens",
        "POST /auth/change-password": "API - Trocar senha (requer token)",
        "POST /images/upload": "API - Fazer upload de imagem (requer token)",
        "DELETE /images/{id}": "API - Deletar própria imagem (requer token)"
    })
    
    # URLs para administradores
    if user.is_admin:
        user_urls.update({
            "GET /admin": "Painel de administração",
            "GET /auth/admin/pending-users": "API - Lista usuários pendentes (requer admin)",
            "POST /auth/admin/approve-user/{id}": "API - Aprovar usuário (requer admin)",
            "POST /auth/admin/reject-user/{id}": "API - Rejeitar usuário (requer admin)",
            "GET /auth/admin/all-users": "API - Lista todos os usuários (requer admin)"
        })
        user_type = "admin"
    else:
        user_type = "user"
    
    return {
        "authenticated": True,
        "user_type": user_type,
        "username": user.username,
        "is_admin": bool(user.is_admin),
        "available_urls": user_urls
    }
