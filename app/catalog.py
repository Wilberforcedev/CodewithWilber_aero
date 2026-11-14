from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Course, LearningPath


COURSES = [
    {
        "slug": "python-foundations",
        "title": "Python Foundations",
        "category": "Python",
        "level": "Beginner",
        "duration": "6 hours",
        "summary": "Build a clear mental model of Python, from first script to useful program.",
        "description": "Learn Python in a deliberate sequence: core syntax, data structures, functions, errors, and small projects that make each idea stick.",
        "outcome": "Create command-line tools and automate everyday tasks.",
        "badge": "Start here",
        "price_label": "Included in the learning plan",
        "featured": True,
    },
    {
        "slug": "python-apis",
        "title": "Python APIs in Practice",
        "category": "Python",
        "level": "Intermediate",
        "duration": "8 hours",
        "summary": "Design, document, and ship dependable APIs with Python.",
        "description": "Move from a working endpoint to a maintainable service with validation, persistence, useful errors, and deployment fundamentals.",
        "outcome": "Build and deploy a documented web API.",
        "badge": "Project course",
        "price_label": "Included in the learning plan",
        "featured": True,
    },
    {
        "slug": "data-analysis-starter",
        "title": "Data Analysis Starter",
        "category": "Data",
        "level": "Beginner",
        "duration": "7 hours",
        "summary": "Turn messy tables into useful, well-explained decisions.",
        "description": "Use Python to clean, explore, and communicate data. Work through a practical analysis from raw file to clear finding.",
        "outcome": "Produce an analysis notebook and shareable findings.",
        "badge": "Popular",
        "price_label": "Included in the learning plan",
        "featured": True,
    },
    {
        "slug": "web-development-basics",
        "title": "Web Development Basics",
        "category": "Web",
        "level": "Beginner",
        "duration": "9 hours",
        "summary": "Understand how modern websites fit together and build one of your own.",
        "description": "Learn the browser, HTTP, HTML, CSS, and the role of a backend by building a responsive, accessible website.",
        "outcome": "Publish a polished first portfolio project.",
        "badge": "Project course",
        "price_label": "Included in the learning plan",
        "featured": False,
    },
    {
        "slug": "sql-for-builders",
        "title": "SQL for Builders",
        "category": "Data",
        "level": "Beginner",
        "duration": "5 hours",
        "summary": "Ask better questions of your data and model it with confidence.",
        "description": "Practice relational thinking, querying, joins, and schema design using realistic application data.",
        "outcome": "Design tables and write useful, maintainable queries.",
        "badge": "Quick win",
        "price_label": "Included in the learning plan",
        "featured": False,
    },
    {
        "slug": "ship-your-first-app",
        "title": "Ship Your First App",
        "category": "Deployment",
        "level": "Intermediate",
        "duration": "4 hours",
        "summary": "Take a small app from your laptop to a reliable live deployment.",
        "description": "Package an application, configure its environment, use a managed database, and understand the checks that matter after launch.",
        "outcome": "Deploy an app with a repeatable release process.",
        "badge": "New skills",
        "price_label": "Included in the learning plan",
        "featured": False,
    },
]

PATHS = [
    {
        "slug": "python-developer",
        "title": "Python Developer",
        "category": "Career path",
        "summary": "Go from Python basics to a dependable service you can show.",
        "description": "A guided sequence through programming fundamentals, API development, data persistence, and a first deployment.",
        "course_slugs": "python-foundations,python-apis,sql-for-builders,ship-your-first-app",
        "duration": "23 hours",
    },
    {
        "slug": "data-practitioner",
        "title": "Data Practitioner",
        "category": "Career path",
        "summary": "Learn to explore data, explain what you found, and make it useful.",
        "description": "Build a practical toolkit for working with data, from querying relational datasets to presenting a clear analysis.",
        "course_slugs": "python-foundations,sql-for-builders,data-analysis-starter",
        "duration": "18 hours",
    },
]


def seed_catalog(db: Session) -> None:
    if db.scalar(select(Course.id).limit(1)) is None:
        db.add_all(Course(**course) for course in COURSES)
    if db.scalar(select(LearningPath.id).limit(1)) is None:
        db.add_all(LearningPath(**path) for path in PATHS)
    db.commit()

