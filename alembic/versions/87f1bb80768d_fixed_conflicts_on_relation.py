"""fixed conflicts on relation

Revision ID: 87f1bb80768d
Revises: d04d6d3e1652
Create Date: 2025-04-11 13:39:49.702397

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '87f1bb80768d'
down_revision: Union[str, None] = 'd04d6d3e1652'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
