"""create user table

Revision ID: af937cbd6092
Revises: 0f1cf186b03d
Create Date: 2023-01-05 13:03:03.157816

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "af937cbd6092"
down_revision = "0f1cf186b03d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("email", sa.String(), nullable=False, unique=True),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("admin", sa.Boolean(), server_default="FALSE", nullable=False),
        sa.Column("validated", sa.Boolean(), server_default="FALSE", nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )


def downgrade() -> None:
    op.drop_column("users")
