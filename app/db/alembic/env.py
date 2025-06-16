import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.db.models import Base
from app.db.session import DATABASE_URL, engine

target_metadata = Base.metadata

def run_migrations_online():
    connectable = engine
    ...
