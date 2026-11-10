"""add orders user created index

Revision ID: c67356032b8e
Revises: 11a7208eb4b1
Create Date: 2026-11-09 20:33:56.244715

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c67356032b8e'
down_revision: Union[str, Sequence[str], None] = '11a7208eb4b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.get_context().autocommit_block():
        op.execute(
            "CREATE INDEX CONCURRENTLY orders_user_created_idx "
            "ON orders (user_id, created_at DESC)"
        )


def downgrade() -> None:
    with op.get_context().autocommit_block():
        op.execute("DROP INDEX CONCURRENTLY orders_user_created_idx")
