from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from supabase import create_client

# Configuração Local (MySQL com SQLAlchemy)
engine_local = create_engine('mysql+pymysql://root:@localhost/persistencia?charset=utf8mb4')
Base = declarative_base()

class Curso(Base):
    __tablename__ = 'curso'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    estudantes = relationship('Estudante', back_populates='curso')

class Estudante(Base):
    __tablename__ = 'estudante'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    curso_id = Column(Integer, ForeignKey('curso.id'))
    curso = relationship('Curso', back_populates='estudantes')

Base.metadata.create_all(engine_local)
SessionLocal = sessionmaker(bind=engine_local)

# Inserir Dados Localmente
def inserir_dados_local(nome_curso, nome_estudante):
    curso_local = Curso(nome=nome_curso)
    estudante_local = Estudante(nome=nome_estudante)

    curso_local.estudantes.append(estudante_local)

    session_local = SessionLocal()
    session_local.add(curso_local)
    session_local.commit()

# Inserir Dados na Nuvem (Supabase)
def inserir_dados_nuvem(nome_curso, nome_estudante):
    supabase_url = 'https://juyfuhcquqbfromnbutz.supabase.co'
    supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imp1eWZ1aGNxdXFiZnJvbW5idXR6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDAwNjQ3OTcsImV4cCI6MjAxNTY0MDc5N30.hk1lD9HxCLp_yEIjsNn1tte1ZGd2nj8KV4ikqVBulAY'

    supabase_client = create_client(supabase_url, supabase_key)

    data_nuvem, count_nuvem = supabase_client.table('curso').upsert([{"nome": nome_curso}]).execute()
    print(data_nuvem)

# Interface de Usuário
def main():
    nome_curso = input("Digite o nome do curso: ")
    nome_estudante = input("Digite o nome do estudante: ")

    inserir_dados_local(nome_curso, nome_estudante)
    inserir_dados_nuvem(nome_curso, nome_estudante)

if __name__ == "__main__":
    main()
