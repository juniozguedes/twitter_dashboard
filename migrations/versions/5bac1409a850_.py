"""empty message

Revision ID: 5bac1409a850
Revises: 
Create Date: 2018-10-17 16:14:56.368595

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5bac1409a850'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('nickname', sa.String(length=30), nullable=True))
    op.drop_column('user', 'name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('name', sa.VARCHAR(length=30), autoincrement=False, nullable=True))
    op.drop_column('user', 'nickname')
    # ### end Alembic commands ###
