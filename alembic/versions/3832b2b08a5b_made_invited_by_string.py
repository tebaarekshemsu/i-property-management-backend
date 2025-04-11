"""made invited by string

Revision ID: 3832b2b08a5b
Revises: 320dda12fb8f
Create Date: 2025-04-11 14:02:45.264823

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3832b2b08a5b'
down_revision: Union[str, None] = '320dda12fb8f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
