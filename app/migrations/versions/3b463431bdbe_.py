"""empty message

Revision ID: 3b463431bdbe
Revises: c2c30983e276
Create Date: 2025-12-27 14:44:18.406484

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3b463431bdbe'
down_revision: Union[str, Sequence[str], None] = 'c2c30983e276'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Добавляем в User_data в колонке id_us_info значение unique=True
    with op.batch_alter_table("user_datas") as batch_op:
        batch_op.create_unique_constraint(
            "uq_user_data_id_us_info",
            ['id_us_info']
        )


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("user_datas") as batch_op:
        batch_op.drop_constraint(
            "uq_user_data_id_us_info",
            type_="unique"
        )