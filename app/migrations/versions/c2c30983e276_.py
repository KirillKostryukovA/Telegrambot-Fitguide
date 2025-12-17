"""empty message

Revision ID: c2c30983e276
Revises: 
Create Date: 2025-12-17 18:25:21.834546

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c2c30983e276'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "user_infos",
        sa.Column("subscription_duration",
        sa.Integer, nullable=True
    ))

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("user_infos", "subscription_duration")
