from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import DBAPIError

Base = declarative_base()

engine = create_engine("postgresql://app_user:app_password@chat_database:5432/app_db")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_session():
    """Função para obter uma sessão do banco de dados."""
    return SessionLocal()

def test_db_connection():
    """Função para testar a conexão com o banco de dados."""
    try:
        with get_session() as session:
            session.execute(text("SELECT 1"))
            print("Conexão com o banco de dados bem-sucedida.")
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")

test_db_connection()

