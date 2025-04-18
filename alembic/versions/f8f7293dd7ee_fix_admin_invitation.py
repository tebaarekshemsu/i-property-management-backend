"""fix admin invitation

Revision ID: f8f7293dd7ee
Revises: eab8427ab3ba
Create Date: 2025-04-18 18:19:36.185579

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f8f7293dd7ee'
down_revision: Union[str, None] = 'eab8427ab3ba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
