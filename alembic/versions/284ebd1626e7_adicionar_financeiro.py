"""adicionar financeiro

Revision ID: 284ebd1626e7
Revises: eebe793ac9ab
Create Date: 2026-11-11 11:10:56.731405

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '284ebd1626e7'
down_revision: Union[str, Sequence[str], None] = 'eebe793ac9ab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    op.add_column(
        "Sessao",
        sa.Column(
            "valor_cobrado",
            sa.Numeric(10, 2),
            nullable=False,
            server_default="0"
        )
    )

    op.create_table(
        "pagamentos",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "sessao_id",
            sa.Integer(),
            sa.ForeignKey("Sessao.id"),
            nullable=False
        ),
        sa.Column(
            "valor",
            sa.Numeric(10, 2),
            nullable=False
        ),
        sa.Column(
            "forma_pagamento",
            sa.String(50),
            nullable=False
        ),
        sa.Column(
            "data_pagamento",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.now()
        ),
        sa.Column("observacao", sa.Text(), nullable=True)
    )
    


def downgrade():
    op.drop_table("pagamentos")
    op.drop_column("Sessao", "valor_cobrado")
