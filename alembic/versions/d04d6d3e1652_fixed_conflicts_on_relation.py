"""fixed conflicts on relation

Revision ID: d04d6d3e1652
Revises: ee43d056eb52
Create Date: 2025-04-11 13:36:55.509540

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd04d6d3e1652'
down_revision: Union[str, None] = 'ee43d056eb52'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
