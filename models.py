from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Float,
    DateTime,
    ForeignKey,
    Text
)

from sqlalchemy.orm import relationship

from database import Base, engine


# =====================================================
# USUÁRIOS
# =====================================================

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False)
    login = Column(String(80), unique=True, nullable=False)
    senha = Column(String(255), nullable=False)
    perfil = Column(String(30), nullable=False)
    ativo = Column(Boolean, default=True)
    criado_em = Column(DateTime, default=datetime.utcnow)


# =====================================================
# PROFESSORES
# =====================================================

class Professor(Base):
    __tablename__ = "professores"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False)
    email = Column(String(150))
    telefone = Column(String(20))

    turmas = relationship("Turma", back_populates="professor")


# =====================================================
# CURSOS
# =====================================================

class Curso(Base):
    __tablename__ = "cursos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(Text)

    turmas = relationship("Turma", back_populates="curso")


# =====================================================
# DISCIPLINAS
# =====================================================

class Disciplina(Base):
    __tablename__ = "disciplinas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False)
    carga_horaria = Column(Integer)

    turmas = relationship("Turma", back_populates="disciplina")


# =====================================================
# TURMAS
# =====================================================

class Turma(Base):
    __tablename__ = "turmas"

    id = Column(Integer, primary_key=True, index=True)

    codigo = Column(String(50))
    serie = Column(String(50))
    turno = Column(String(30))
    ano = Column(Integer)

    curso_id = Column(Integer, ForeignKey("cursos.id"))
    professor_id = Column(Integer, ForeignKey("professores.id"))
    disciplina_id = Column(Integer, ForeignKey("disciplinas.id"))

    curso = relationship("Curso", back_populates="turmas")
    professor = relationship("Professor", back_populates="turmas")
    disciplina = relationship("Disciplina", back_populates="turmas")

    alunos = relationship(
        "Aluno",
        back_populates="turma",
        cascade="all, delete-orphan"
    )


# =====================================================
# ALUNOS
# =====================================================

class Aluno(Base):
    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True, index=True)

    numero = Column(Integer)
    nome = Column(String(200), nullable=False)
    matricula = Column(String(50), unique=True)

    turma_id = Column(Integer, ForeignKey("turmas.id"))

    turma = relationship("Turma", back_populates="alunos")

    notas = relationship(
        "Nota",
        back_populates="aluno",
        cascade="all, delete-orphan"
    )

    presencas = relationship(
        "Presenca",
        back_populates="aluno",
        cascade="all, delete-orphan"
    )

    resultado_final = relationship(
        "ResultadoFinal",
        back_populates="aluno",
        uselist=False,
        cascade="all, delete-orphan"
    )


# =====================================================
# NOTAS
# =====================================================

class Nota(Base):
    __tablename__ = "notas"

    id = Column(Integer, primary_key=True, index=True)

    trimestre = Column(Integer)

    nm1 = Column(Float)
    nm2 = Column(Float)
    nm3 = Column(Float)

    media = Column(Float)
    recuperacao = Column(Float)
    media_final = Column(Float)

    aluno_id = Column(Integer, ForeignKey("alunos.id"))

    aluno = relationship("Aluno", back_populates="notas")


# =====================================================
# RESULTADO FINAL
# =====================================================

class ResultadoFinal(Base):
    __tablename__ = "resultados_finais"

    id = Column(Integer, primary_key=True, index=True)

    media_anual = Column(Float)
    prova_final = Column(Float)
    media_final = Column(Float)
    recuperacao_final = Column(Float)

    faltas = Column(Integer)

    situacao = Column(String(30))

    aluno_id = Column(Integer, ForeignKey("alunos.id"))

    aluno = relationship(
        "Aluno",
        back_populates="resultado_final"
    )


# =====================================================
# PRESENÇAS
# =====================================================

class Presenca(Base):
    __tablename__ = "presencas"

    id = Column(Integer, primary_key=True, index=True)

    data = Column(
        DateTime,
        default=datetime.utcnow
    )

    presente = Column(Boolean)

    aluno_id = Column(Integer, ForeignKey("alunos.id"))

    aluno = relationship(
        "Aluno",
        back_populates="presencas"
    )


# =====================================================
# IMPORTAÇÕES
# =====================================================

class Importacao(Base):
    __tablename__ = "importacoes"

    id = Column(Integer, primary_key=True, index=True)

    arquivo = Column(String(255))

    professor = Column(String(150))
    disciplina = Column(String(150))
    turma = Column(String(100))

    serie = Column(String(50))
    ano = Column(Integer)

    data_importacao = Column(
        DateTime,
        default=datetime.utcnow
    )


# =====================================================
# CRIAR BANCO
# =====================================================

def criar_banco():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    criar_banco()
    print("Banco criado com sucesso!")