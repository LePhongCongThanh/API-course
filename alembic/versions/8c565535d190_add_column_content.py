"""add column content

Revision ID: 8c565535d190
Revises: cf5fee4670e0
Create Date: 2023-06-18 13:02:04.756975

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8c565535d190'
down_revision = 'cf5fee4670e0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content",sa.String(255), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts","content")
    pass
