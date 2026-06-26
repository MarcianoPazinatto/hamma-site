from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, Form, Header
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import shutil
from datetime import datetime

from ..database import get_db
from ..models import User, Image
from ..schemas import ImageResponse, ImageWithOwner, ImageCreate
from ..auth import decode_token
from ..services import cloudinary_service

router = APIRouter(prefix="/images", tags=["images"])

UPLOAD_DIRECTORY = "app/static/uploads"

# Criar diretório de uploads se não existir
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)


def get_current_user(token: str = None, db: Session = None) -> User:
    """Obtém o usuário atual do token JWT"""
    if token is None:
        return None
    
    username = decode_token(token)
    if username is None:
        return None
    
    user = db.query(User).filter(User.username == username).first()
    return user


@router.get("/", response_model=List[ImageWithOwner])
def list_images(db: Session = Depends(get_db)):
    """Lista todas as imagens"""
    images = db.query(Image).order_by(Image.created_at.desc()).all()
    return images


@router.get("/my-images", response_model=List[ImageWithOwner])
def list_my_images(
    db: Session = Depends(get_db),
    token: Optional[str] = None
):
    """Lista apenas as imagens do usuário autenticado"""
    if not token:
        return []
    
    user = get_current_user(token, db)
    if not user:
        return []
    
    images = db.query(Image).filter(Image.owner_id == user.id).order_by(Image.created_at.desc()).all()
    return images


@router.post("/upload", response_model=ImageResponse)
async def upload_image(
    title: str = Form(...),
    value: float = Form(...),
    description: str = Form(default=""),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    token: str = None
):
    """Faz upload de uma imagem (apenas usuários autenticados)"""
    # Verificar autenticação
    if token is None:
        raise HTTPException(status_code=401, detail="Token não fornecido")
    
    user = get_current_user(token, db)
    if user is None:
        raise HTTPException(status_code=401, detail="Não autenticado")

    # Validar arquivo
    if file.content_type not in ["image/jpeg", "image/png", "image/gif", "image/webp"]:
        raise HTTPException(status_code=400, detail="Formato de imagem inválido")

    # Fazer upload para Cloudinary
    cloudinary_url, public_id = await cloudinary_service.upload_image(file)

    # Salvar no banco de dados
    db_image = Image(
        title=title,
        description=description,
        value=value,
        filename=None,  # Não usar filename local mais
        cloudinary_url=cloudinary_url,
        cloudinary_public_id=public_id,
        owner_id=user.id
    )
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    
    return db_image


@router.put("/{image_id}", response_model=ImageResponse)
async def update_image(
    image_id: int,
    title: str = Form(None),
    value: float = Form(None),
    description: str = Form(None),
    file: UploadFile = File(None),
    db: Session = Depends(get_db),
    token: str = None
):
    """Edita uma imagem (qualquer usuário logado pode editar qualquer imagem)"""
    if token is None:
        raise HTTPException(status_code=401, detail="Token não fornecido")
    
    user = get_current_user(token, db)
    if user is None:
        raise HTTPException(status_code=401, detail="Não autenticado")

    image = db.query(Image).filter(Image.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Imagem não encontrada")

    # Atualizar apenas os campos que foram realmente enviados
    # O frontend envia apenas os campos que foram alterados
    if title is not None and title.strip():
        image.title = title.strip()
    
    if description is not None:
        image.description = description.strip()
    
    if value is not None and value > 0:
        image.value = float(value)

    # Atualizar arquivo se fornecido
    if file and file.filename:
        # Validar novo arquivo
        if file.content_type not in ["image/jpeg", "image/png", "image/gif", "image/webp"]:
            raise HTTPException(status_code=400, detail="Formato de imagem inválido")

        # Deletar arquivo antigo do Cloudinary
        if image.cloudinary_public_id:
            await cloudinary_service.delete_image(image.cloudinary_public_id)

        # Fazer upload do novo arquivo
        cloudinary_url, public_id = await cloudinary_service.upload_image(file)
        
        image.cloudinary_url = cloudinary_url
        image.cloudinary_public_id = public_id
        image.filename = None

    db.commit()
    db.refresh(image)
    
    return image


@router.delete("/{image_id}")
async def delete_image(
    image_id: int,
    db: Session = Depends(get_db),
    token: str = None
):
    """Deleta uma imagem (qualquer usuário logado pode deletar qualquer imagem)"""
    if token is None:
        raise HTTPException(status_code=401, detail="Token não fornecido")
    
    user = get_current_user(token, db)
    if user is None:
        raise HTTPException(status_code=401, detail="Não autenticado")

    image = db.query(Image).filter(Image.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Imagem não encontrada")

    # Deletar imagem do Cloudinary
    if image.cloudinary_public_id:
        await cloudinary_service.delete_image(image.cloudinary_public_id)

    # Deletar do banco de dados
    db.delete(image)
    db.commit()

    return {"message": "Imagem deletada com sucesso"}
