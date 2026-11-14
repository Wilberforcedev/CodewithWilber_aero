"""Create course and learning path catalog tables."""

from alembic import op
import sqlalchemy as sa

revision = "20261114_01"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "courses",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("slug", sa.String(length=100), nullable=False),
        sa.Column("title", sa.String(length=160), nullable=False),
        sa.Column("category", sa.String(length=80), nullable=False),
        sa.Column("level", sa.String(length=40), nullable=False),
        sa.Column("duration", sa.String(length=40), nullable=False),
        sa.Column("summary", sa.String(length=240), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("outcome", sa.String(length=200), nullable=False),
        sa.Column("badge", sa.String(length=40), nullable=False, server_default=""),
        sa.Column("price_label", sa.String(length=60), nullable=False, server_default="Included in the learning plan"),
        sa.Column("featured", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.UniqueConstraint("slug", name="uq_courses_slug"),
    )
    op.create_index("ix_courses_title", "courses", ["title"])
    op.create_index("ix_courses_category", "courses", ["category"])
    op.create_table(
        "learning_paths",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("slug", sa.String(length=100), nullable=False),
        sa.Column("title", sa.String(length=160), nullable=False),
        sa.Column("category", sa.String(length=80), nullable=False),
        sa.Column("summary", sa.String(length=240), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("course_slugs", sa.Text(), nullable=False),
        sa.Column("duration", sa.String(length=40), nullable=False),
        sa.UniqueConstraint("slug", name="uq_learning_paths_slug"),
    )
    op.create_index("ix_learning_paths_title", "learning_paths", ["title"])


def downgrade() -> None:
    op.drop_index("ix_learning_paths_title", table_name="learning_paths")
    op.drop_table("learning_paths")
    op.drop_index("ix_courses_category", table_name="courses")
    op.drop_index("ix_courses_title", table_name="courses")
    op.drop_table("courses")
