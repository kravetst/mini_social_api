from fastapi import FastAPI
from app.routers import post, user, auth
from app.core.redis import connect_redis, close_redis

app = FastAPI()


@app.on_event("startup")
async def startup():
    await connect_redis()


@app.on_event("shutdown")
async def shutdown():
    await close_redis()


app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)
