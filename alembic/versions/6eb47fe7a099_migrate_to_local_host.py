"""migrate to local host

Revision ID: 6eb47fe7a099
Revises: 9a5705ca6384
Create Date: 2025-04-05 22:13:12.432036

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6eb47fe7a099'
down_revision: Union[str, None] = '9a5705ca6384'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
