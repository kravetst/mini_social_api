# Mini Social API

Mini Social API is a training project to demonstrate the basic functionality of a social network: user registration and authorization, post creation, likes, caching, and basic rate limiting.

## Technologies

- Python 3.11
- FastAPI - web framework
- SQLAlchemy (Async) – ORM for working with databases
- PostgreSQL – database
- Alembic – database migrations
- Redis – post caching and limits
- Pydantic – data validation and serialization
- Docker & Docker Compose – containerization


## 📁 Project structure

```bash
mini_social_api/
├─ app/
│  ├─ main.py                  # FastAPI entry point
│  ├─ models/                  # SQLAlchemy DB Models
│  ├─ schemas/                 # Pydantic-schemes
│  ├─ services/                # Business process logic
│  ├─ repositories/            # Work with DB
│  ├─ routers/                 # API routers
│  └─ core/                    # Configuration, dependencies, Redis, security
├─ alembic/                    # Database migrations
├─ requirements.txt            # Packages Python
├─ docker-compose.yml          # Config Docker
├─ Dockerfile                  # Docker image
└─ README.md
```
## ⚡ Local setup

1. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/Scripts/activate
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Configure .env (if necessary) to connect to PostgreSQL and Redis.
4. Perform migrations and update the database:

```bash
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```
5. Run the application:

```bash
uvicorn app.main:app --reload
```
The API will be available at: http://127.0.0.1:8000

---
## 🐳 Running with Docker

1. Build Docker image:
```bash
docker build -t mini_social_api .
```
2. Start containers:
```bash
docker-compose up -d
```
3. Run migrations inside container:
```bash
docker-compose exec web alembic upgrade head
```

## 🧩 Main endpoints
Authorization

- POST /auth/register – user registration
- POST /auth/login – login, returns access and refresh tokens
- GET /auth/me – get current user

Posts

- POST /posts/ – create a post
- GET /posts/ – get list of posts (supports pagination, search and sorting)
- GET /posts/{post_id} – get post by ID
- POST /posts/{post_id}/like – like/unlike

Users

- GET /users/ – get list of users

## 💾 Caching & Rate limits

Redis caches post list (TTL 30s)

Rate limiting for likes

## ⚠️ Notes

Unit tests not connected yet

Use .env to configure DB and Redis