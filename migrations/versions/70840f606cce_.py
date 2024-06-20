"""empty message

Revision ID: 70840f606cce
Revises: 
Create Date: 2024-06-14 17:57:14.133160

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '70840f606cce'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.Column('password_hash', sa.String(length=200), nullable=True),
    sa.Column('experience', sa.Integer(), nullable=True),
    sa.Column('city', sa.String(length=50), nullable=True),
    sa.Column('role', sa.Enum('Admin', 'Moderator', 'Employer', 'Employee', name='role'), nullable=True),
    sa.Column('confirmed', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('name')
    )
    op.create_table('companies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('description', sa.String(length=150), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('projects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('description', sa.String(length=150), nullable=True),
    sa.Column('features', sa.String(length=150), nullable=True),
    sa.Column('prog_languages', sa.String(length=50), nullable=True),
    sa.Column('link', sa.String(length=150), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('projects')
    op.drop_table('companies')
    op.drop_table('users')
    # ### end Alembic commands ###