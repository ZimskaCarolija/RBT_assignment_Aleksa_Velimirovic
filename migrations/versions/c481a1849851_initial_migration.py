"""Initial migration

Revision ID: c481a1849851
Revises: 
Create Date: 2025-11-07 21:44:39.517983

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = 'c481a1849851'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Roles
    op.create_table(
        'roles',
        sa.Column('id', sa.SmallInteger(), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False, unique=True),
        sa.Index('ix_roles_name', 'name', unique=True)
    )

    # Users
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('password', sa.String(255), nullable=False),
        sa.Column('full_name', sa.String(255), nullable=True),
        sa.Column('role_id', sa.SmallInteger(), sa.ForeignKey('roles.id'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Index('ix_users_email', 'email', unique=True)
    )

    # Vacation Entitlements
    op.create_table(
        'vacation_entitlements',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('year', sa.SmallInteger(), nullable=False),
        sa.Column('total_days', sa.SmallInteger(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint('user_id', 'year', name='uq_user_year')
    )

    # Vacation Records
    op.create_table(
        'vacation_records',
        sa.Column('id', sa.Integer(), primary_key=True),  # PROMENJENO: Integer umesto SmallInteger
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),  # PROMENJENO
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=False),
        sa.Column('days_count', sa.SmallInteger(), nullable=False),
        sa.Column('year', sa.SmallInteger(), nullable=False),
        sa.Column('note', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False),
    )


def downgrade():
    op.drop_table('vacation_records')
    op.drop_table('vacation_entitlements')
    op.drop_table('users')
    op.drop_table('roles')