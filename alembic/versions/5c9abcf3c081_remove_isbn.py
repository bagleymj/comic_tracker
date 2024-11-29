"""Remove ISBN

Revision ID: 5c9abcf3c081
Revises: 10d8c2b33f82
Create Date: 2024-11-28 21:34:51.490865

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5c9abcf3c081'
down_revision: Union[str, None] = '10d8c2b33f82'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('books', 'isbn')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('books', sa.Column('isbn', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
