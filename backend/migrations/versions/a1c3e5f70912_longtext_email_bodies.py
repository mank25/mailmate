"""longtext email bodies

Revision ID: a1c3e5f70912
Revises: e86f540d2829
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.mysql import LONGTEXT

revision: str = 'a1c3e5f70912'
down_revision: Union[str, Sequence[str], None] = 'e86f540d2829'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    for col in ("body_text", "body_html"):
        op.alter_column("emails", col, existing_type=sa.Text(), type_=LONGTEXT(), existing_nullable=True)


def downgrade() -> None:
    for col in ("body_text", "body_html"):
        op.alter_column("emails", col, existing_type=LONGTEXT(), type_=sa.Text(), existing_nullable=True)
