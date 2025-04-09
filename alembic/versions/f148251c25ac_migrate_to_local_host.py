"""migrate to local host

Revision ID: f148251c25ac
Revises: 2531913a8b6e
Create Date: 2025-04-05 22:04:27.262509

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f148251c25ac'
down_revision: Union[str, None] = '2531913a8b6e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
