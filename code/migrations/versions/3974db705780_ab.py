"""ab

Revision ID: 3974db705780
Revises: 
Create Date: 2021-06-15 19:45:07.372959

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3974db705780'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('note',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('note', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('note')
    # ### end Alembic commands ###
