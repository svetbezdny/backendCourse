"""add bookings

Revision ID: 061a89dad981
Revises: 6bd174939dc4
Create Date: 2025-02-25 23:13:03.256304

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "061a89dad981"
down_revision: Union[str, None] = "6bd174939dc4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "bookings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("room_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("date_from", sa.Date(), nullable=False),
        sa.Column("date_to", sa.Date(), nullable=False),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["room_id"],
            ["rooms.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("bookings")
