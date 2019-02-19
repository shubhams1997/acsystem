"""empty message

Revision ID: f9cc504ffdd7
Revises: eacb94fc5641
Create Date: 2019-02-19 22:23:04.044055

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f9cc504ffdd7'
down_revision = 'eacb94fc5641'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('supplier',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=40), nullable=False),
    sa.Column('first', sa.String(length=40), nullable=True),
    sa.Column('last', sa.String(length=40), nullable=True),
    sa.Column('mailingname', sa.String(length=40), nullable=True),
    sa.Column('address', sa.String(length=100), nullable=True),
    sa.Column('country', sa.String(length=30), nullable=True),
    sa.Column('state', sa.String(length=30), nullable=True),
    sa.Column('pin', sa.Integer(), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.Column('phoneno', sa.Integer(), nullable=True),
    sa.Column('gstno', sa.Integer(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('supplier')
    # ### end Alembic commands ###
