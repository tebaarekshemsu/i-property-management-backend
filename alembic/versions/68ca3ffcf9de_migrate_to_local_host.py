"""migrate to local host

Revision ID: 68ca3ffcf9de
Revises: 696ecb25dc71
Create Date: 2025-04-05 22:02:48.767599

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '68ca3ffcf9de'
down_revision: Union[str, None] = '696ecb25dc71'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
