""" create post table

Revision ID: cf5fee4670e0
Revises: 
Create Date: 2023-06-18 12:49:54.380087

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cf5fee4670e0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("Post_user", sa.Column("ID",sa.Integer, nullable=False, primary_key=True, autoincrement=True),
                    sa.Column("title", sa.String(255), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table("Post_user")
    pass