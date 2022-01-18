"""create urls table

Revision ID: c661f232bb7d
Revises: 27eae880fb1b
Create Date: 2022-01-18 12:24:20.863650

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c661f232bb7d'
down_revision = '27eae880fb1b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "urls",
        sa.Column("id", sa.BigInteger, primary_key=True),
        sa.Column("original_url", sa.Text, nullable=False),
        sa.Column("user_id", sa.BigInteger, sa.ForeignKey("users.id")),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.current_timestamp()),
        sa.Column("updated_at", sa.DateTime, server_default=sa.func.current_timestamp())
    )
    op.create_index("urls_user_id_idx", "urls", ["user_id"])


def downgrade():
    op.drop_table("urls")
