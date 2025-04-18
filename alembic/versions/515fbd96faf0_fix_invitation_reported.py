"""fix invitation reported

Revision ID: 515fbd96faf0
Revises: 63bd5117b710
Create Date: 2025-04-18 20:04:34.532197

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '515fbd96faf0'
down_revision: Union[str, None] = '63bd5117b710'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
