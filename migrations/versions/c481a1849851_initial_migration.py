"""Initial migration

Revision ID: c481a1849851
Revises: 
Create Date: 2025-11-07 21:44:39.517983

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c481a1849851'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'roles',
        sa.Column('id', sa.SmallInteger, primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
    )

    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('password', sa.String(255), nullable=False),
        sa.Column('full_name', sa.String(255), nullable=True),
        sa.Column('role_id', sa.SmallInteger, sa.ForeignKey('roles.id'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        'vacation_entitlements',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('year', sa.SmallInteger, nullable=False),
        sa.Column('total_days', sa.SmallInteger, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint('user_id', 'year', name='uq_user_year')
    )


    op.create_table(
        'vacation_records',
        sa.Column('id', sa.SmallInteger, primary_key=True),
        sa.Column('user_id', sa.SmallInteger, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('start_date', sa.Date, nullable=False),
        sa.Column('end_date', sa.Date, nullable=False),
        sa.Column('days_count', sa.SmallInteger, nullable=False),
        sa.Column('year', sa.SmallInteger, nullable=False),
        sa.Column('note', sa.Text, nullable=True),
    )


def downgrade():
    op.drop_table('vacation_records')
    op.drop_table('vacation_entitlements')
    op.drop_table('users')
    op.drop_table('roles')
