import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

# Carrega o .env da pasta backend/ independente de onde o uvicorn for chamado
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")


class DatabaseConfig:
    """Centraliza as configurações de conexão com o banco de dados."""

    def __init__(self, url: str | None = None):
        self.url: str = url or os.getenv(
            "DATABASE_URL",
            "postgresql://postgres:postgres@localhost:5432/empresas_db"
        )
        self._engine = create_engine(self.url)
        self._SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self._engine
        )

    @property
    def engine(self):
        return self._engine

    def get_session(self) -> sessionmaker:
        return self._SessionLocal

    def create_tables(self, base) -> None:
        """Cria todas as tabelas mapeadas no Base fornecido."""
        base.metadata.create_all(bind=self._engine)


# Instância única (Singleton)
db_config = DatabaseConfig()

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """Dependency do FastAPI: fornece uma sessão e garante o fechamento."""
    db: Session = db_config.get_session()()
    try:
        yield db
    finally:
        db.close()
