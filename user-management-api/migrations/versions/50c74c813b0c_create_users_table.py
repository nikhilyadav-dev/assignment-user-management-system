"""Create users table

Revision ID: 50c74c813b0c
Revises:
Create Date: 2026-09-26 15:49:02.886641
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "50c74c813b0c"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )


def downgrade():
    op.drop_table("users")