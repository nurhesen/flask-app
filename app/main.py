 # app/main.py
from fastapi import FastAPI, Depends
from app.api.routes import auth, posts
from app.db.session import get_db
# Import create_test_db and drop_test_db functions
from app.db.test_db import create_test_db, drop_test_db

app = FastAPI()

# Include your API routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(posts.router, prefix="/posts", tags=["posts"])

# Startup event to create the database tables
@app.on_event("startup")
async def startup_event():
    # Commented next line
    # Base.metadata.create_all(bind=engine)
    pass

# Shutdown event.
@app.on_event("shutdown")
async def shutdown_event():
    pass