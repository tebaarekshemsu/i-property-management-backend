"""updating house table making image url to array 

Revision ID: ed8f3dd11b45
Revises: 7f284129da7e
Create Date: 2025-03-14 09:20:31.927383

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ed8f3dd11b45'
down_revision: Union[str, None] = '7f284129da7e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('house', sa.Column('image_urls', sa.ARRAY(sa.Text()), nullable=True))
    op.drop_column('house', 'photo')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('house', sa.Column('photo', sa.TEXT(), autoincrement=False, nullable=True))
    op.drop_column('house', 'image_urls')
    # ### end Alembic commands ###
