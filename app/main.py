from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine
from routers import post, user, auth, votes
from config import settings

#defining the database instance and connection
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# my_posts = [{"title" : "title of post 1", "content" : "content of post 1", "id"  : 1}, {"title" : "Favourite food" , "content" : "Mutton", "id" : 2}]

# def find_post(id):
#     for i in my_posts:
#         if i["id"] == id:
#             return i

# def find_index_post(id):
#     for i,p in enumerate(my_posts):
#         if p['id'] == id:
#             return i


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)

@app.get('/')
def root():
    return {'message':'Hello world'}