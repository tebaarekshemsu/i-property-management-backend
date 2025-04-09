"""add password column to admin

Revision ID: 4d2eb8b4ffe2
Revises: 715010b4dd50
Create Date: 2025-04-05 00:15:25.180446

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4d2eb8b4ffe2'
down_revision: Union[str, None] = '715010b4dd50'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
