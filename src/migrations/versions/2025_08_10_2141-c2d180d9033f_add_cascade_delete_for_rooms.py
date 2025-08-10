"""add cascade delete for rooms

Revision ID: c2d180d9033f
Revises: 2f7a3078aa61
Create Date: 2025-08-10 21:41:48.403750

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "c2d180d9033f"
down_revision: Union[str, None] = "2f7a3078aa61"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
