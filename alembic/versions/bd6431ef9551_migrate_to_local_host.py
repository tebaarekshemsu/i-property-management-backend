"""migrate to local host

Revision ID: bd6431ef9551
Revises: 8214a036ce6c
Create Date: 2025-04-05 21:59:39.169099

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bd6431ef9551'
down_revision: Union[str, None] = '8214a036ce6c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
