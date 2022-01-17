"""create users table

Revision ID: 70aceb19f9d0
Revises: 
Create Date: 2022-01-17 18:37:27.956549

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '70aceb19f9d0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.BigInteger, primary_key=True),
        sa.Column("login", sa.String(255), nullable=False, unique=True),
        sa.Column("password", sa.Text, nullable=False),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.current_timestamp()),
        sa.Column("updated_at", sa.DateTime, server_default=sa.func.current_timestamp())
    )


def downgrade():
    op.drop_table("users")