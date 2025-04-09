"""migrate to local host

Revision ID: 0d618452dbab
Revises: bd6431ef9551
Create Date: 2025-04-05 22:01:09.421280

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0d618452dbab'
down_revision: Union[str, None] = 'bd6431ef9551'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
