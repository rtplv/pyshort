"""create tokens table

Revision ID: 27eae880fb1b
Revises: 70aceb19f9d0
Create Date: 2022-01-17 18:37:31.702098

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '27eae880fb1b'
down_revision = '70aceb19f9d0'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "tokens",
        sa.Column("id", sa.BigInteger, primary_key=True),
        sa.Column("token", sa.Text, nullable=False),
        sa.Column("user_id", sa.BigInteger, sa.ForeignKey("users.id")),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.current_timestamp()),
        sa.Column("updated_at", sa.DateTime, server_default=sa.func.current_timestamp()),
    )
    op.create_index("tokens_user_id_idx", "tokens", ["user_id"])


def downgrade():
    op.drop_table("tokens")

