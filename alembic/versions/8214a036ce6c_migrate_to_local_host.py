"""migrate to local host

Revision ID: 8214a036ce6c
Revises: 4d2eb8b4ffe2
Create Date: 2025-04-05 21:42:35.947070

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8214a036ce6c'
down_revision: Union[str, None] = '4d2eb8b4ffe2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
