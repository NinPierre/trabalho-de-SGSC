from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Enum,
    Float,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship

from database import Base


# ==========================
# USUÁRIO
# ==========================
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(150), nullable=False)
    login = Column(String(50), unique=True, nullable=False)
    senha = Column(String(225), nullable=False)

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


# ==========================
# PROFESSOR
# ==========================
class Professor(Base):
    __tablename__ = "professor"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(150), nullable=False)
    matricula = Column(String(30), unique=True)
    email = Column(String(150))
    telefone = Column(String(20))

    disciplinas = relationship("Disciplina", back_populates="professor")


# ==========================
# CURSO
# ==========================
class Curso(Base):
    __tablename__ = "curso"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(String(255))

    disciplinas = relationship("Disciplina", back_populates="curso")


# ==========================
# DISCIPLINA
# ==========================
class Disciplina(Base):
    __tablename__ = "disciplina"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    carga_horaria = Column(Integer)

    professor_id = Column(Integer, ForeignKey("professor.id"))
    curso_id = Column(Integer, ForeignKey("curso.id"))

    professor = relationship("Professor", back_populates="disciplinas")
    curso = relationship("Curso", back_populates="disciplinas")

    notas = relationship("Nota", back_populates="disciplina")


# ==========================
# TURMA
# ==========================
class Turma(Base):
    __tablename__ = "turma"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)

    alunos = relationship("Aluno", back_populates="turma")


# ==========================
# ALUNO
# ==========================
class Aluno(Base):
    __tablename__ = "aluno"

    id = Column(Integer, primary_key=True, autoincrement=True)

    nome = Column(String(150), nullable=False)
    matricula = Column(String(30), unique=True)
    email = Column(String(150))
    telefone = Column(String(20))

    turma_id = Column(Integer, ForeignKey("turma.id"))

    ativo = Column(Boolean, default=True)
    data_cadastro = Column(DateTime, default=datetime.utcnow)

    turma = relationship("Turma", back_populates="alunos")

    notas = relationship("Nota", back_populates="aluno")

    resultado = relationship(
        "ResultadoFinal",
        back_populates="aluno",
        uselist=False
    )

    def __repr__(self):
        return f"<Aluno {self.nome}>"


# ==========================
# NOTA
# ==========================
class Nota(Base):
    __tablename__ = "nota"

    id = Column(Integer, primary_key=True, autoincrement=True)

    aluno_id = Column(Integer, ForeignKey("aluno.id"))
    disciplina_id = Column(Integer, ForeignKey("disciplina.id"))

    bimestre = Column(Integer)
    nota = Column(Float)

    aluno = relationship("Aluno", back_populates="notas")
    disciplina = relationship("Disciplina", back_populates="notas")


# ==========================
# RESULTADO FINAL
# ==========================
class ResultadoFinal(Base):
    __tablename__ = "resultado_final"

    id = Column(Integer, primary_key=True, autoincrement=True)

    aluno_id = Column(Integer, ForeignKey("aluno.id"))

    media = Column(Float)
    situacao = Column(String(20))

    aluno = relationship("Aluno", back_populates="resultado")