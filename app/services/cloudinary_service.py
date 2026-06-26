"""
Serviço para integração com Cloudinary
Responsável por upload, deleção e gerenciamento de imagens no Cloudinary
"""

import cloudinary
import cloudinary.uploader
from typing import Tuple, Optional
from fastapi import UploadFile, HTTPException
from ..config import get_settings


def init_cloudinary():
    """Inicializa a configuração do Cloudinary"""
    settings = get_settings()
    
    if not settings.CLOUDINARY_CLOUD_NAME:
        raise ValueError("CLOUDINARY_CLOUD_NAME não está configurado")
    
    cloudinary.config(
        cloud_name=settings.CLOUDINARY_CLOUD_NAME,
        api_key=settings.CLOUDINARY_API_KEY,
        api_secret=settings.CLOUDINARY_API_SECRET
    )


async def upload_image(file: UploadFile) -> Tuple[str, str]:
    """
    Faz upload de uma imagem para o Cloudinary
    
    Args:
        file: UploadFile do FastAPI
    
    Returns:
        Tuple[str, str]: (cloudinary_url, public_id)
    
    Raises:
        HTTPException: Se houver erro no upload
    """
    try:
        init_cloudinary()
        
        # Ler conteúdo do arquivo
        file_content = await file.read()
        
        # Fazer upload para Cloudinary com pasta específica
        result = cloudinary.uploader.upload(
            file_content,
            folder="hama-sharing",  # Pasta no Cloudinary
            resource_type="auto"
        )
        
        cloudinary_url = result.get("secure_url")
        public_id = result.get("public_id")
        
        if not cloudinary_url or not public_id:
            raise HTTPException(
                status_code=500,
                detail="Erro ao processar resposta do Cloudinary"
            )
        
        return cloudinary_url, public_id
        
    except cloudinary.exceptions.Error as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao fazer upload no Cloudinary: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro inesperado durante upload: {str(e)}"
        )


async def delete_image(public_id: str) -> bool:
    """
    Deleta uma imagem do Cloudinary
    
    Args:
        public_id: ID público da imagem no Cloudinary
    
    Returns:
        bool: True se deletado com sucesso
    
    Raises:
        HTTPException: Se houver erro na deleção
    """
    try:
        if not public_id:
            return True  # Se não há public_id, considerar como sucesso
        
        init_cloudinary()
        
        result = cloudinary.uploader.destroy(public_id)
        
        if result.get("result") == "ok":
            return True
        else:
            # Log do erro mas não falha a operação
            print(f"Aviso: Cloudinary retornou resultado não esperado para {public_id}: {result}")
            return True  # Continuar mesmo que não tenha deletado
        
    except cloudinary.exceptions.Error as e:
        # Logar erro mas não falhar a deleção do registro
        print(f"Erro ao deletar imagem do Cloudinary: {str(e)}")
        return True
    except Exception as e:
        # Logar erro mas não falhar a deleção do registro
        print(f"Erro inesperado ao deletar imagem: {str(e)}")
        return True
