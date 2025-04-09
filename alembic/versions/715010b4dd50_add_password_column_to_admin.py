"""add password column to admin

Revision ID: 715010b4dd50
Revises: ed8f3dd11b45
Create Date: 2025-04-04 23:55:57.409156

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '715010b4dd50'
down_revision: Union[str, None] = 'ed8f3dd11b45'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
