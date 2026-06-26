"""Add cloudinary_url and cloudinary_public_id columns to images table

Revision ID: 001
Revises: 
Create Date: 2026-06-26 14:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Check if images table exists
    ctx = op.get_context()
    inspector = ctx.get_bind().inspector
    
    # Get existing columns
    try:
        columns = inspector.get_columns('images')
        column_names = [col['name'] for col in columns]
    except Exception:
        # Table might not exist yet, which is fine
        column_names = []
    
    # Adicionar coluna cloudinary_url se não existir
    if 'cloudinary_url' not in column_names:
        op.add_column('images', sa.Column('cloudinary_url', sa.String(), nullable=True))
    
    # Adicionar coluna cloudinary_public_id se não existir
    if 'cloudinary_public_id' not in column_names:
        op.add_column('images', sa.Column('cloudinary_public_id', sa.String(), nullable=True))


def downgrade() -> None:
    ctx = op.get_context()
    inspector = ctx.get_bind().inspector
    
    # Get existing columns
    try:
        columns = inspector.get_columns('images')
        column_names = [col['name'] for col in columns]
    except Exception:
        column_names = []
    
    # Remove columns if they exist
    if 'cloudinary_public_id' in column_names:
        op.drop_column('images', 'cloudinary_public_id')
    
    if 'cloudinary_url' in column_names:
        op.drop_column('images', 'cloudinary_url')
