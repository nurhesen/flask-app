"""initial migration

Revision ID: abcdef123456
Revises: 
Create Date: 2025-03-15 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'abcdef123456'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('email', sa.String(255), unique=True, index=True, nullable=False),
        sa.Column('hashed_password', sa.String(255), nullable=False)
    )
    # Create posts table
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('text', sa.String(1024), nullable=False),
        sa.Column('user_id', sa.Integer, sa.ForeignKey("users.id"), nullable=False)
    )

def downgrade():
    op.drop_table('posts')
    op.drop_table('users')
