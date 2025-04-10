"""fixed owner

Revision ID: daba814a415a
Revises: 84a34c0c9994
Create Date: 2025-04-09 22:25:07.736684

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'daba814a415a'
down_revision: Union[str, None] = '84a34c0c9994'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
