"""migrate to local host

Revision ID: 05275d360f93
Revises: 68ca3ffcf9de
Create Date: 2025-04-05 22:03:16.032174

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '05275d360f93'
down_revision: Union[str, None] = '68ca3ffcf9de'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
