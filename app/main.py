from fastapi import FastAPI
from routes import user,auth
from db.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(user.router,prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])