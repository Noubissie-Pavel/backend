"""telecom_operator migration unique

Revision ID: ab30c10447ce
Revises: 69812d43c73a
Create Date: 2025-02-27 11:43:05.886241

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ab30c10447ce'
down_revision: Union[str, None] = '69812d43c73a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('telecom_operator', 'description',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('telecom_operator', 'description',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
