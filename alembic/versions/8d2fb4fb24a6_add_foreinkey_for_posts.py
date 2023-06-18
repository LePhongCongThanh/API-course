"""add foreinkey for posts'

Revision ID: 8d2fb4fb24a6
Revises: c7015a968f50
Create Date: 2023-06-18 14:30:03.259496

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8d2fb4fb24a6'
down_revision = 'c7015a968f50'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # op.add_column("posts", sa.Column("owner_id", sa.Integer,
    #                                   sa.ForeignKey("users.ID_user", ondelete="CASCADE"), nullable=False))
    op.add_column("Post_user", sa.Column("owner_id", sa.Integer, nullable=False))
    op.create_foreign_key("posts_ibfk_1", source_table="Post_user", referent_table="Users",
                          local_cols=["owner_id"], remote_cols=["ID_user"], ondelete="CASCADE")
    pass


def downgrade() -> None:
    # op.drop_column("posts", "owner_id")
    op.drop_constraint("posts_ibfk_1", table_name="Post_user", type_="foreignkey")
    op.drop_column("Post_user", "owner_id")
    pass
