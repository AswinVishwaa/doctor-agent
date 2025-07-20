from db.models import Base
from db.database import engine

# Run this once to create tables
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)