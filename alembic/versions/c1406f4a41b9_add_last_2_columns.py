"""add last 2 columns

Revision ID: c1406f4a41b9
Revises: 8d2fb4fb24a6
Create Date: 2023-06-18 15:01:28.896168

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c1406f4a41b9'
down_revision = '8d2fb4fb24a6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("Post_user", sa.Column("name", sa.String(255), nullable=False))
    op.add_column("Post_user", sa.Column("published", sa.Boolean, nullable=False, server_default="1"))
    op.add_column("Post_user", sa.Column("rating", sa.Integer, nullable=False, server_default="2"))
    op.add_column("Post_user", sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False,
                                      server_default=sa.text("now()")))
    pass


def downgrade() -> None:
    op.drop_column("Post_user", "name")
    op.drop_column("Post_user", "published")
    op.drop_column("Post_user", "rating")
    op.drop_column("Post_user", "created_at")
    pass
