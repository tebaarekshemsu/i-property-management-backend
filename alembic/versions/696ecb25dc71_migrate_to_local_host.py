"""migrate to local host

Revision ID: 696ecb25dc71
Revises: 0d618452dbab
Create Date: 2025-04-05 22:01:43.074425

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '696ecb25dc71'
down_revision: Union[str, None] = '0d618452dbab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
