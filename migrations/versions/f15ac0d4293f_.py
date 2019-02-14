"""empty message

Revision ID: f15ac0d4293f
Revises: 5840ae3fcde6
Create Date: 2019-02-14 13:43:46.185527

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f15ac0d4293f'
down_revision = '5840ae3fcde6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'company', type_='foreignkey')
    op.create_foreign_key(None, 'company', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'company', type_='foreignkey')
    op.create_foreign_key(None, 'company', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###