"""fix admin invitation

Revision ID: baf9f7e3862f
Revises: 97bdb9155a4c
Create Date: 2025-04-18 18:10:18.030242

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'baf9f7e3862f'
down_revision: Union[str, None] = '97bdb9155a4c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
