"""migrate to local host

Revision ID: 2531913a8b6e
Revises: 05275d360f93
Create Date: 2025-04-05 22:03:58.498817

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2531913a8b6e'
down_revision: Union[str, None] = '05275d360f93'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
