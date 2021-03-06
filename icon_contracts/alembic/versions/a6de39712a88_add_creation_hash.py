"""add creation hash

Revision ID: a6de39712a88
Revises: aef5033f1f49
Create Date: 2021-11-16 00:13:16.367371

"""
import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision = "a6de39712a88"
down_revision = "aef5033f1f49"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "contracts", sa.Column("creation_hash", sqlmodel.sql.sqltypes.AutoString(), nullable=True)
    )
    op.drop_index("ix_contracts_owner_address", table_name="contracts")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index("ix_contracts_owner_address", "contracts", ["owner_address"], unique=False)
    op.drop_column("contracts", "creation_hash")
    # ### end Alembic commands ###
