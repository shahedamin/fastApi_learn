from database import engine,base,SessionLocal
import models

def create_db():
    return base.metadata.create_all(bind=engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


# create_db()