"""migrate to local host

Revision ID: 84a34c0c9994
Revises: 6eb47fe7a099
Create Date: 2025-04-05 22:20:30.689213

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '84a34c0c9994'
down_revision: Union[str, None] = '6eb47fe7a099'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
