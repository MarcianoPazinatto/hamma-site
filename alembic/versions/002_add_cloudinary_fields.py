"""Add cloudinary fields to images table

Revision ID: 002
Revises: 001
Create Date: 2026-06-26 14:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Check if columns already exist to avoid duplicate column errors
    try:
        op.add_column('images', sa.Column('cloudinary_url', sa.String(), nullable=True))
    except Exception:
        pass  # Column might already exist
    
    try:
        op.add_column('images', sa.Column('cloudinary_public_id', sa.String(), nullable=True))
    except Exception:
        pass  # Column might already exist


def downgrade() -> None:
    op.drop_column('images', 'cloudinary_public_id')
    op.drop_column('images', 'cloudinary_url')
