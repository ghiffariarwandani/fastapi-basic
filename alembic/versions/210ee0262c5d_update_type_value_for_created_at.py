"""update type & value for created_at

Revision ID: 210ee0262c5d
Revises: 9504b6ca99df
Create Date: 2026-02-14 17:30:43.488957

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "210ee0262c5d"
down_revision: Union[str, Sequence[str], None] = "9504b6ca99df"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table("product", recreate="always") as batch_op:
        batch_op.alter_column(
            "created_at",
            existing_type=sa.String(),
            type_=sa.DateTime(),
            existing_nullable=False,
        )


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("product", recreate="always") as batch_op:
        batch_op.alter_column(
            "created_at",
            existing_type=sa.DateTime(),
            type_=sa.String(),
            existing_nullable=False,
        )
