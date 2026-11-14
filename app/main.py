import logging
from contextlib import asynccontextmanager
from pathlib import Path
from urllib.parse import quote

from fastapi import Depends, FastAPI, HTTPException, Query, Request
from fastapi.responses import PlainTextResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import func, select, text
from sqlalchemy.orm import Session

from app.catalog import seed_catalog
from app.config import get_settings
from app.db import SessionLocal, get_db
from app.models import Course, LearningPath

settings = get_settings()
APP_DIR = Path(__file__).resolve().parent
logging.basicConfig(level=settings.log_level.upper(), format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger = logging.getLogger("wilber")


@asynccontextmanager
async def lifespan(_: FastAPI):
    with SessionLocal() as db:
        seed_catalog(db)
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan, docs_url=None, redoc_url=None)
app.mount("/static", StaticFiles(directory=APP_DIR / "static"), name="static")
templates = Jinja2Templates(directory=APP_DIR / "templates")


@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    response.headers.setdefault("X-Frame-Options", "DENY")
    response.headers.setdefault("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
    response.headers.setdefault("Content-Security-Policy", "default-src 'self'; img-src 'self' data:; style-src 'self' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; script-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self' mailto:")
    if settings.environment == "production":
        response.headers.setdefault("Strict-Transport-Security", "max-age=63072000; includeSubDomains")
    return response


def page_context(request: Request, **values):
    return {"request": request, "settings": settings, **values}


@app.get("/", name="home")
def home(request: Request, db: Session = Depends(get_db)):
    courses = db.scalars(select(Course).where(Course.featured.is_(True)).order_by(Course.id)).all()
    paths = db.scalars(select(LearningPath).order_by(LearningPath.id)).all()
    course_count = db.scalar(select(func.count()).select_from(Course)) or 0
    return templates.TemplateResponse("home.html", page_context(request, courses=courses, paths=paths, course_count=course_count))


@app.get("/courses", name="courses")
def courses(
    request: Request,
    q: str = Query(default="", max_length=100),
    category: str = Query(default="", max_length=80),
    db: Session = Depends(get_db),
):
    query = select(Course).order_by(Course.featured.desc(), Course.title)
    if q.strip():
        term = f"%{q.strip()}%"
        query = query.where(Course.title.ilike(term) | Course.summary.ilike(term) | Course.category.ilike(term))
    if category.strip():
        query = query.where(Course.category == category.strip())
    items = db.scalars(query).all()
    categories = db.scalars(select(Course.category).distinct().order_by(Course.category)).all()
    return templates.TemplateResponse("courses.html", page_context(request, courses=items, categories=categories, q=q, category=category))


@app.get("/courses/{slug}", name="course_detail")
def course_detail(request: Request, slug: str, db: Session = Depends(get_db)):
    course = db.scalar(select(Course).where(Course.slug == slug))
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return templates.TemplateResponse("course_detail.html", page_context(request, course=course))


@app.get("/learning-paths", name="learning_paths")
def learning_paths(request: Request, db: Session = Depends(get_db)):
    paths = db.scalars(select(LearningPath).order_by(LearningPath.title)).all()
    return templates.TemplateResponse("paths.html", page_context(request, paths=paths))


@app.get("/learning-paths/{slug}", name="learning_path_detail")
def learning_path_detail(request: Request, slug: str, db: Session = Depends(get_db)):
    path = db.scalar(select(LearningPath).where(LearningPath.slug == slug))
    if path is None:
        raise HTTPException(status_code=404, detail="Learning path not found")
    slugs = [value for value in path.course_slugs.split(",") if value]
    course_map = {course.slug: course for course in db.scalars(select(Course).where(Course.slug.in_(slugs))).all()}
    path_courses = [course_map[value] for value in slugs if value in course_map]
    return templates.TemplateResponse("path_detail.html", page_context(request, path=path, courses=path_courses))


@app.get("/health", name="health")
def health(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        logger.exception("Database health check failed")
        raise HTTPException(status_code=503, detail="Database unavailable") from None
    return {"status": "ok", "database": "ok"}


@app.get("/robots.txt", response_class=PlainTextResponse)
def robots():
    return f"User-agent: *\nAllow: /\nSitemap: {settings.site_url.rstrip('/')}/sitemap.xml\n"


@app.get("/sitemap.xml")
def sitemap(db: Session = Depends(get_db)):
    origin = settings.site_url.rstrip("/")
    urls = [f"{origin}/", f"{origin}/courses", f"{origin}/learning-paths"]
    urls.extend(f"{origin}/courses/{quote(slug)}" for slug in db.scalars(select(Course.slug)).all())
    urls.extend(f"{origin}/learning-paths/{quote(slug)}" for slug in db.scalars(select(LearningPath.slug)).all())
    body = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">"
    body += "".join(f"<url><loc>{url}</loc></url>" for url in urls)
    body += "</urlset>"
    return Response(content=body, media_type="application/xml")
