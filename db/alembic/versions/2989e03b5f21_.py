"""empty message

Revision ID: 2989e03b5f21
Revises: 3c842c2aa107
Create Date: 2022-08-30 13:55:26.020966

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2989e03b5f21'
down_revision = '3c842c2aa107'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('description', sa.String(length=1000), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('products', 'description')
    # ### end Alembic commands ###