"""deleted users table

Revision ID: 320dda12fb8f
Revises: 87f1bb80768d
Create Date: 2025-04-11 13:53:01.858645

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '320dda12fb8f'
down_revision: Union[str, None] = '87f1bb80768d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
