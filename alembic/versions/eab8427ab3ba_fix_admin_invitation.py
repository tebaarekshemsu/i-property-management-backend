"""fix admin invitation

Revision ID: eab8427ab3ba
Revises: baf9f7e3862f
Create Date: 2025-04-18 18:12:01.536772

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eab8427ab3ba'
down_revision: Union[str, None] = 'baf9f7e3862f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
