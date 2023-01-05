"""create booking table

Revision ID: 0f1cf186b03d
Revises: 
Create Date: 2023-01-05 12:49:27.565028

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0f1cf186b03d"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "bookings",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("start_date", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column("end_date", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column("number_of_people", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("validated", sa.Boolean(), server_default="FALSE", nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )


def downgrade() -> None:
    op.drop_table("bookings")
