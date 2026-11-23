"""Add country and anonymous session fields to visitor events."""

import sqlalchemy as sa

from alembic import op

revision = "0002_analytics_privacy_fields"
down_revision = "0001_initial_schema"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "visitor_events", sa.Column("country_code", sa.String(2), nullable=True)
    )
    op.add_column(
        "visitor_events",
        sa.Column("session_id_hash", sa.String(128), nullable=True),
    )
    op.create_index(
        "ix_visitor_events_session_id_hash",
        "visitor_events",
        ["session_id_hash"],
    )


def downgrade() -> None:
    op.drop_index("ix_visitor_events_session_id_hash", table_name="visitor_events")
    op.drop_column("visitor_events", "session_id_hash")
    op.drop_column("visitor_events", "country_code")
