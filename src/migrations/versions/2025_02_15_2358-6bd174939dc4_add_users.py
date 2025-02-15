"""add users

Revision ID: 6bd174939dc4
Revises: 4736fa6a4a0a
Create Date: 2025-02-15 23:58:37.533008

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6bd174939dc4"
down_revision: Union[str, None] = "4736fa6a4a0a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=True),
        sa.Column("email", sa.String(length=100), nullable=False),
        sa.Column("age", sa.Integer(), nullable=False),
        sa.Column("city", sa.String(), nullable=True),
        sa.Column("hashed_password", sa.String(length=200), nullable=False),
        sa.CheckConstraint("age > 0 AND age <= 150", name="users_age_check"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )


def downgrade() -> None:
    op.drop_table("users")
