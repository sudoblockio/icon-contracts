"""change contract_type meaning and add token standard

Revision ID: 038b6ed909a1
Revises: 80b5d1f25196
Create Date: 2022-06-13 09:19:28.961577

"""
import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision = "038b6ed909a1"
down_revision = "80b5d1f25196"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "contracts", sa.Column("token_standard", sqlmodel.sql.sqltypes.AutoString(), nullable=True)
    )
    op.drop_index("ix_contracts_address", table_name="contracts")
    op.create_index(
        op.f("ix_contracts_token_standard"), "contracts", ["token_standard"], unique=False
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_contracts_token_standard"), table_name="contracts")
    op.create_index("ix_contracts_address", "contracts", ["address"], unique=False)
    op.drop_column("contracts", "token_standard")
    # ### end Alembic commands ###