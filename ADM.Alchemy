from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import sessionmaker
from sqlalchemy import func

from seu_arquivo_unico import (
    engine,
    SessionLocal,
    Usuario,
    Professor,
    Curso,
    Disciplina,
    Turma,
    Aluno,
    Nota,
    ResultadoFinal,
    Presenca,
    Importacao
)

Session = sessionmaker(bind=engine)
session = Session()


# ==========================
# ADMINISTRAÇÃO: USUÁRIO
# ==========================
def criar_usuario(nome, login, senha, perfil):
    novo_usuario = Usuario(
        nome=nome,
        login=login,
        senha=senha,
        perfil=perfil
    )
    session.add(novo_usuario)
    session.commit()
    return novo_usuario


def desativar_usuario(usuario_id):
    usuario = session.query(Usuario).filter_by(id=usuario_id).first()
    if usuario:
        usuario.ativo = False
        session.commit()
    return usuario


# ==========================
# ADMINISTRAÇÃO: PROFESSOR
# ==========================
def cadastrar_professor(nome, matricula, email, telefone):
    novo_professor = Professor(
        nome=nome,
        matricula=matricula,
        email=email,
        telefone=telefone
    )
    session.add(novo_professor)
    session.commit()
    return novo_professor


# ==========================
# ADMINISTRAÇÃO: CURSO
# ==========================
def criar_curso(nome, descricao):
    novo_curso = Curso(
        nome=nome,
        descricao=descricao
    )
    session.add(novo_curso)
    session.commit()
    return novo_curso


# ==========================
# ADMINISTRAÇÃO: DISCIPLINA
# ==========================
def criar_disciplina(nome, carga_horaria):
    nova_disciplina = Disciplina(
        nome=nome,
        carga_horaria=carga_horaria
    )
    session.add(nova_disciplina)
    session.commit()
    return nova_disciplina


# ==========================
# ADMINISTRAÇÃO: TURMA
# ==========================
def criar_turma(codigo, serie, turno, ano, curso_id, professor_id, disciplina_id):
    nova_turma = Turma(
        codigo=codigo,
        serie=serie,
        turno=turno,
        ano=ano,
        curso_id=curso_id,
        professor_id=professor_id,
        disciplina_id=disciplina_id
    )
    session.add(nova_turma)
    session.commit()
    return nova_turma


# ==========================
# ADMINISTRAÇÃO: ALUNO
# ==========================
def matricular_aluno(numero, nome, matricula, turma_id):
    novo_aluno = Aluno(
        numero=numero,
        nome=nome,
        matricula=matricula,
        turma_id=turma_id
    )
    session.add(novo_aluno)
    session.commit()
    return novo_aluno


# ==========================
# ADMINISTRAÇÃO: NOTA
# ==========================
def lancar_nota(aluno_id, trimestre, nm1, nm2, nm3, recuperacao=None):
    n1 = Decimal(str(nm1)) if nm1 is not None else Decimal('0.0')
    n2 = Decimal(str(nm2)) if nm2 is not None else Decimal('0.0')
    n3 = Decimal(str(nm3)) if nm3 is not None else Decimal('0.0')
    
    media = (n1 + n2 + n3) / Decimal('3.0')
    media = round(media, 1)
    
    media_final = media
    if recuperacao is not None:
        rec = Decimal(str(recuperacao))
        if rec > media:
            media_final = rec

    nova_nota = Nota(
        aluno_id=aluno_id,
        trimestre=trimestre,
        nm1=n1,
        nm2=n2,
        nm3=n3,
        media=media,
        recuperacao=recuperacao,
        media_final=media_final
    )
    session.add(nova_nota)
    session.commit()
    return nova_nota


# ==========================
# ADMINISTRAÇÃO: PRESENÇA
# ==========================
def registrar_presenca(aluno_id, data, presente):
    nova_presenca = Presenca(
        aluno_id=aluno_id,
        data=data,
        presente=presente
    )
    session.add(nova_presenca)
    session.commit()
    return nova_presenca


# ==========================
# ADMINISTRAÇÃO: RESULTADO
# ==========================
def calcular_resultado_final(aluno_id, prova_final, recuperacao_final, faltas):
    aluno = session.query(Aluno).filter_by(id=aluno_id).first()
    if not aluno:
        return None

    notas_aluno = session.query(Nota).filter_by(aluno_id=aluno_id).all()
    
    if len(notas_aluno) > 0:
        soma_medias = sum(Decimal(str(n.media_final)) for n in notas_aluno)
        media_anual = soma_medias / Decimal(str(len(notas_aluno)))
        media_anual = round(media_anual, 1)
    else:
        media_anual = Decimal('0.0')

    pf = Decimal(str(prova_final)) if prova_final is not None else Decimal('0.0')
    rf = Decimal(str(recuperacao_final)) if recuperacao_final is not None else Decimal('0.0')

    media_final = (media_anual + pf) / Decimal('2.0')
    media_final = round(media_final, 1)

    if rf > media_final:
        media_final = rf

    if faltas > 20:
        situacao = "REPROVADO POR FALTA"
    elif media_final >= Decimal('7.0'):
        situacao = "APROVADO"
    else:
        situacao = "REPROVADO"

    resultado = ResultadoFinal(
        aluno_id=aluno_id,
        media_anual=media_anual,
        prova_final=prova_final,
        media_final=media_final,
        recuperacao_final=recuperacao_final,
        faltas=faltas,
        situacao=situacao
    )
    session.add(resultado)
    session.commit()
    return resultado


# ==========================
# ADMINISTRAÇÃO: IMPORTAÇÃO
# ==========================
def registrar_importacao(arquivo, professor, disciplina, turma, serie, ano, usuario_id):
    nova_importacao = Importacao(
        arquivo=arquivo,
        professor=professor,
        disciplina=disciplina,
        turma=turma,
        serie=serie,
        ano=ano,
        usuario_id=usuario_id
    )
    session.add(nova_importacao)
    session.commit()
    return nova_importacao


# ==========================
# ADMINISTRAÇÃO: RANKINGS
# ==========================
def gerar_ranking_da_turma(turma_id):
    ranking = session.query(
        Aluno.nome,
        func.avg(Nota.media_final).label("desempenho_medio")
    ).join(Nota, Aluno.id == Nota.aluno_id)\
     .filter(Aluno.turma_id == turma_id)\
     .group_by(Aluno.id)\
     .order_by(func.avg(Nota.media_final).desc())\
     .all()
    return ranking


def gerar_ranking_geral_das_turmas():
    ranking_turmas = session.query(
        Turma.codigo,
        func.avg(Nota.media_final).label("media_geral_turma")
    ).join(Aluno, Turma.id == Aluno.turma_id)\
     .join(Nota, Aluno.id == Nota.aluno_id)\
     .group_by(Turma.id)\
     .order_by(func.avg(Nota.media_final).desc())\
     .all()
    return ranking_turmas


# ==========================
# ADMINISTRAÇÃO: CONSULTAS
# ==========================
def obter_boletim(aluno_id):
    aluno = session.query(Aluno).filter_by(id=aluno_id).first()
    if not aluno:
        return None
        
    notas = session.query(Nota).filter_by(aluno_id=aluno_id).all()
    resultado = session.query(ResultadoFinal).filter_by(aluno_id=aluno_id).first()
    presencas = session.query(Presenca).filter_by(aluno_id=aluno_id).all()
    
    return {
        "aluno": aluno,
        "notas": notas,
        "resultado_final": resultado,
        "presencas": presencas
    }
