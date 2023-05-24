from database import engine,base

def create_db():
    return base.metadata.create_all(bind=engine)

create_db()