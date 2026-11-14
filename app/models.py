from sqlalchemy import Boolean, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True)
    title: Mapped[str] = mapped_column(String(160), index=True)
    category: Mapped[str] = mapped_column(String(80), index=True)
    level: Mapped[str] = mapped_column(String(40))
    duration: Mapped[str] = mapped_column(String(40))
    summary: Mapped[str] = mapped_column(String(240))
    description: Mapped[str] = mapped_column(Text)
    outcome: Mapped[str] = mapped_column(String(200))
    badge: Mapped[str] = mapped_column(String(40), default="")
    price_label: Mapped[str] = mapped_column(String(60), default="Included in the learning plan")
    featured: Mapped[bool] = mapped_column(Boolean, default=False)


class LearningPath(Base):
    __tablename__ = "learning_paths"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True)
    title: Mapped[str] = mapped_column(String(160), index=True)
    category: Mapped[str] = mapped_column(String(80))
    summary: Mapped[str] = mapped_column(String(240))
    description: Mapped[str] = mapped_column(Text)
    course_slugs: Mapped[str] = mapped_column(Text)
    duration: Mapped[str] = mapped_column(String(40))

