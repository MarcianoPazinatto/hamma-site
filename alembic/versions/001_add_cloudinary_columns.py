"""Add cloudinary_url and cloudinary_public_id columns to images table

Revision ID: 001
Revises: 
Create Date: 2026-06-26 14:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Adicionar coluna cloudinary_url
    op.add_column('images', sa.Column('cloudinary_url', sa.String(), nullable=True))
    
    # Adicionar coluna cloudinary_public_id
    op.add_column('images', sa.Column('cloudinary_public_id', sa.String(), nullable=True))
    
    # Fazer filename nullable para compatibilidade
    op.alter_column('images', 'filename',
               existing_type=sa.String(),
               nullable=True)


def downgrade() -> None:
    # Reverter as mudanças se necessário
    op.drop_column('images', 'cloudinary_public_id')
    op.drop_column('images', 'cloudinary_url')
    
    op.alter_column('images', 'filename',
               existing_type=sa.String(),
               nullable=False)
