"""migrate to local host

Revision ID: 9a5705ca6384
Revises: f148251c25ac
Create Date: 2025-04-05 22:06:18.836140

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9a5705ca6384'
down_revision: Union[str, None] = 'f148251c25ac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
