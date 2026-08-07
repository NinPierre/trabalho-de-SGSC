from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Banco local SQLite
DATABASE_URL = "sqlite:///liceu.db"

# Cria a conexão
engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False}
)

# Cria a sessão
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base para os modelos
Base = declarative_base()