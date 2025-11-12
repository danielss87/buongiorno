"""
Buongiorno API - Database Configuration
Configuração do SQLAlchemy e gerenciamento de sessões
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

try:
    from .config import DATABASE_URL, SQLALCHEMY_ECHO
except ImportError:
    from config import DATABASE_URL, SQLALCHEMY_ECHO

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    echo=SQLALCHEMY_ECHO,
    connect_args={'check_same_thread': False} if 'sqlite' in DATABASE_URL else {}
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency para obter sessão do banco de dados
    Usado no FastAPI para injeção de dependência

    Yields:
        Session: Sessão do SQLAlchemy

    Example:
        @app.get("/items/")
        def read_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Inicializa o banco de dados
    Cria todas as tabelas definidas nos models
    """
    # Import all models so they are registered with Base
    try:
        from . import models
    except ImportError:
        import models

    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("Banco de dados inicializado!")


def drop_db():
    """
    Remove todas as tabelas do banco de dados
    CUIDADO: Usar apenas em desenvolvimento!
    """
    Base.metadata.drop_all(bind=engine)
    print("Todas as tabelas foram removidas!")


def reset_db():
    """
    Reseta o banco de dados (drop + create)
    CUIDADO: Usar apenas em desenvolvimento!
    """
    drop_db()
    init_db()
    print("Banco de dados resetado!")
