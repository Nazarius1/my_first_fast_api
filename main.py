from fastapi import FastAPI
import models
from database import engine
from routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware



#tables would be recreated if not exists
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

# @app.get("/")
# async def root():
#     return {"message": "Hello World! API is ready!"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# here is where the routers are wired to main
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

