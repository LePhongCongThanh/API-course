"""create user table'

Revision ID: c7015a968f50
Revises: 8c565535d190
Create Date: 2023-06-18 13:22:41.179637

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import null, text


# revision identifiers, used by Alembic.
revision = 'c7015a968f50'
down_revision = '8c565535d190'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("users",
                    sa.Column("ID_user", sa.Integer, primary_key=True, nullable=False, autoincrement=True),
                    sa.Column("Name", sa.String(255), nullable=False),
                    sa.Column("Password",sa.String(255), nullable=False),
                    sa.Column("Email", sa.String(255), nullable=False, unique=True),
                    sa.Column("created_at", TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")))
    

    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
