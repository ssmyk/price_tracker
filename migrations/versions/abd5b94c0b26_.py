"""empty message

Revision ID: abd5b94c0b26
Revises: eb8ac8729d20
Create Date: 2022-02-27 23:07:52.236445

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'abd5b94c0b26'
down_revision = 'eb8ac8729d20'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('current_price_date', sa.DateTime(), nullable=True))
    op.add_column('products', sa.Column('lowest_price_date', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('products', 'lowest_price_date')
    op.drop_column('products', 'current_price_date')
    # ### end Alembic commands ###