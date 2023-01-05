from . import models
from .database import engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import booking, user, auth, validation
from .config import settings

# models.Base.metadata.create_all(bind=engine) # use to create the tables without alembic

origins = ["*"]  # secure which website can access my API.

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(booking.router)
app.include_router(user.router)
app.include_router(validation.router)


@app.get("/")
def root():
    return {"message": "Hello World !"}


#    12h05 : https://www.freecodecamp.org/news/creating-apis-with-python-free-19-hour-course/
# uvicorn app.main:app --reload
# c:/Users/Guillaume/Documents/code/fastapi/venv/Scripts/Activate.ps1


# Sur la MV pour activer la machine virtuel : cd app puis source venv/bin/activate
# pip install -r requirement.txt
# crééer une environnemen variable export VAR = .. /unset / printenv
#  set -o allexport; source /home/guillaume/.env; set +o allexport

# gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
