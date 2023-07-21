"""Add fields to taxonomy tables

Revision ID: ab3ca78f611e
Revises: 8593edebb67a
Create Date: 2023-07-20 23:29:18.528369

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ab3ca78f611e"
down_revision = "8593edebb67a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("iip_forms", sa.Column("ana", sa.String(), nullable=True))
    op.add_column("iip_writings", sa.Column("note", sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("iip_writings", "note")
    op.drop_column("iip_forms", "ana")
    # ### end Alembic commands ###
