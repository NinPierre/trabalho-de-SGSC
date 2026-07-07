from datetime import datetime

from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    String,
    Boolean,
    Enum,
    Numeric,
    DateTime,
    Text,
    ForeignKey,
    Index,
    create_engine
)

from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = " INSIRA_A_URL_DO_SEU_BANCO_AQUI "

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


# ==========================
# USUÁRIO
# ==========================
class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nome = Column(String(150), nullable=False)
    login = Column(String(50), unique=True, nullable=False)
    senha = Column(String(255), nullable=False)

    perfil = Column(
        Enum(
            "ADMIN",
            "COORDENADOR",
            "PROFESSOR",
            name="perfil_usuario"
        ),
        nullable=False
    )

    ativo = Column(Boolean, default=True)
    criado_em = Column(DateTime, default=datetime.utcnow)

    importacoes = relationship("Importacao", back_populates="usuario")


# ==========================
# PROFESSOR
# ==========================
class Professor(Base):
    __tablename__ = "professor"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nome = Column(String(150), nullable=False)
    matricula = Column(String(30))
    email = Column(String(150))
    telefone = Column(String(20))

    turmas = relationship("Turma", back_populates="professor")


# ==========================
# CURSO
# ==========================
class Curso(Base):
    __tablename__ = "curso"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(Text)

    turmas = relationship("Turma", back_populates="curso")


# ==========================
# DISCIPLINA
# ==========================
class Disciplina(Base):
    __tablename__ = "disciplina"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nome = Column(String(150))
    carga_horaria = Column(Integer)

    turmas = relationship("Turma", back_populates="disciplina")


# ==========================
# TURMA
# ==========================
class Turma(Base):
    __tablename__ = "turma"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    codigo = Column(String(60))
    serie = Column(String(50))
    turno = Column(String(30))
    ano = Column(Integer)

    curso_id = Column(BigInteger, ForeignKey("curso.id"))
    professor_id = Column(BigInteger, ForeignKey("professor.id"))
    disciplina_id = Column(BigInteger, ForeignKey("disciplina.id"))

    curso = relationship("Curso", back_populates="turmas")
    professor = relationship("Professor", back_populates="turmas")
    disciplina = relationship("Disciplina", back_populates="turmas")
    alunos = relationship("Aluno", back_populates="turma")


# ==========================
# ALUNO
# ==========================
class Aluno(Base):
    __tablename__ = "aluno"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    numero = Column(Integer)
    nome = Column(String(200), nullable=False)
    matricula = Column(String(30))

    turma_id = Column(BigInteger, ForeignKey("turma.id"))

    turma = relationship("Turma", back_populates="alunos")
    notas = relationship("Nota", back_populates="aluno")
    resultados_finais = relationship("ResultadoFinal", back_populates="aluno")
    presencas = relationship("Presenca", back_populates="aluno")


# ==========================
# NOTA
# ==========================
class Nota(Base):
    __tablename__ = "nota"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    aluno_id = Column(BigInteger, ForeignKey("aluno.id"), nullable=False)
    trimestre = Column(Integer)

    nm1 = Column(Numeric(4, 1))
    nm2 = Column(Numeric(4, 1))
    nm3 = Column(Numeric(4, 1))
    media = Column(Numeric(4, 1))
    recuperacao = Column(Numeric(4, 1))
    media_final = Column(Numeric(4, 1))

    aluno = relationship("Aluno", back_populates="notas")


# ==========================
# RESULTADO FINAL
# ==========================
class ResultadoFinal(Base):
    __tablename__ = "resultado_final"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    aluno_id = Column(BigInteger, ForeignKey("aluno.id"))

    media_anual = Column(Numeric(4, 1))
    prova_final = Column(Numeric(4, 1))
    media_final = Column(Numeric(4, 1))
    recuperacao_final = Column(Numeric(4, 1))
    faltas = Column(Integer)
    situacao = Column(String(20))

    aluno = relationship("Aluno", back_populates="resultados_finais")


# ==========================
# PRESENÇA
# ==========================
class Presenca(Base):
    __tablename__ = "presenca"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    aluno_id = Column(BigInteger, ForeignKey("aluno.id"), nullable=False)
    data = Column(DateTime, default=datetime.utcnow)
    presente = Column(Boolean, nullable=False)

    aluno = relationship("Aluno", back_populates="presencas")


# ==========================
# IMPORTAÇÃO
# ==========================
class Importacao(Base):
    __tablename__ = "importacao"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    arquivo = Column(String(255))
    professor = Column(String(150))
    disciplina = Column(String(150))
    turma = Column(String(100))
    serie = Column(String(50))
    ano = Column(Integer)
    data_importacao = Column(DateTime, default=datetime.utcnow)

    usuario_id = Column(BigInteger, ForeignKey("usuario.id"))

    usuario = relationship("Usuario", back_populates="importacoes")


Index("idx_aluno_nome", Aluno.nome)
Index("idx_turma", Turma.codigo)
Index("idx_importacao", Importacao.data_importacao)


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas com sucesso!")