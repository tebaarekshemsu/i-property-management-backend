"""fixed conflicts on relation

Revision ID: ee43d056eb52
Revises: daba814a415a
Create Date: 2025-04-11 13:35:13.313040

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ee43d056eb52'
down_revision: Union[str, None] = 'daba814a415a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
