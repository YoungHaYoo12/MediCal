"""Add PushSubscription model.

Revision ID: 97c4b12df3b0
Revises: 6704d826efa2
Create Date: 2020-07-17 10:27:14.688661

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '97c4b12df3b0'
down_revision = '6704d826efa2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('push_subscription',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('subscription_json', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('push_subscription')
    # ### end Alembic commands ###
