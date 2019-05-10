"""empty message

Revision ID: 55cb0367fd69
Revises: ae0ddfe503db
Create Date: 2019-05-10 19:33:33.050268

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '55cb0367fd69'
down_revision = 'ae0ddfe503db'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_profile', sa.Column('isAdmin', sa.String(length=6), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_profile', 'isAdmin')
    # ### end Alembic commands ###
