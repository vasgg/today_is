"""initial_revision

Revision ID: 5fd5925da995
Revises:
Create Date: 2025-07-13 21:18:05.964549

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "5fd5925da995"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("firstname", sa.String(), nullable=True),
        sa.Column("lastname", sa.String(), nullable=True),
        sa.Column("username", sa.String(length=32), nullable=True),
        sa.Column("language_code", sa.String(), nullable=True),
        sa.Column("utc_offset", sa.Integer(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
    )
    op.create_table(
        "records",
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("event_name", sa.String(length=4096), nullable=True),
        sa.Column("event_date", sa.DateTime(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.user_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("records")
    op.drop_table("users")
