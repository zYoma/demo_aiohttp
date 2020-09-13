"""Initial

Revision ID: e9ebc7463119
Revises: eb65f446d6b6
Create Date: 2020-09-13 11:17:29.561125

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e9ebc7463119'
down_revision = 'eb65f446d6b6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('desc', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'desc')
    # ### end Alembic commands ###
