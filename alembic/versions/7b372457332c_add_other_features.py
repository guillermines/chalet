"""add other features

Revision ID: 7b372457332c
Revises: af937cbd6092
Create Date: 2023-01-05 13:15:33.812002

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7b372457332c'
down_revision = 'af937cbd6092'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('validations',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('booking_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['booking_id'], ['bookings.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'booking_id')
    )
    op.add_column('bookings', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'bookings', 'users', ['owner_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'bookings', type_='foreignkey')
    op.drop_column('bookings', 'owner_id')
    op.drop_table('validations')
    # ### end Alembic commands ###
