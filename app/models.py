from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Integer, default=0)  # 0 = inativo, 1 = ativo (aprovado)
    is_admin = Column(Integer, default=0)  # 0 = usuário comum, 1 = administrador
    created_at = Column(DateTime, default=datetime.utcnow)

    images = relationship("Image", back_populates="owner")


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    value = Column(Float)
    filename = Column(String, unique=True, index=True, nullable=True)  # Mantido para compatibilidade
    cloudinary_url = Column(String, nullable=True)  # URL da imagem no Cloudinary
    cloudinary_public_id = Column(String, nullable=True)  # ID público para deleção
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="images")
