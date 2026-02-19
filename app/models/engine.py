from sqlmodel import Session, create_engine

engine = create_engine("sqlite:///inventory.db")

def get_db():
    with Session(engine) as session:
        yield session
