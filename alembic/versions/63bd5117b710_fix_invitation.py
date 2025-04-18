"""fix invitation

Revision ID: 63bd5117b710
Revises: f8f7293dd7ee
Create Date: 2025-04-18 18:28:05.068488

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '63bd5117b710'
down_revision: Union[str, None] = 'f8f7293dd7ee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
