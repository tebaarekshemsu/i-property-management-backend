"""made invited by string

Revision ID: 97bdb9155a4c
Revises: 3832b2b08a5b
Create Date: 2025-04-11 22:53:59.851802

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '97bdb9155a4c'
down_revision: Union[str, None] = '3832b2b08a5b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
