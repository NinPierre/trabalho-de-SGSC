from flask import Blueprint, render_template, session

import adm as db
from src.blueprints.auth import login_required

aluno_bp = Blueprint("aluno_bp", __name__)


def contexto_usuario(perfil):
    nome = session.get("nome") or "Usuário"
    return {"nome": nome, "nome_usuario": nome, "perfil": perfil}


@aluno_bp.route("/aluno/inicio", endpoint="aluno_inicio")
@login_required("aluno")
def aluno_inicio():
    return render_template("Aluno-inicial.html", **contexto_usuario("aluno"))


@aluno_bp.route("/aluno/ver-notas", endpoint="aluno_notas")
@login_required("aluno")
def aluno_notas():
    boletim = db.obter_boletim(session.get("usuario_id"))
    return render_template("Aluno-notas.html", boletim=boletim, **contexto_usuario("aluno"))


@aluno_bp.route("/aluno/ranking-das-turmas", endpoint="ranking_turmas")
@login_required("aluno")
def ranking_turmas():
    ranking_turmas_dados = db.gerar_ranking_geral_das_turmas()
    return render_template("Ranking-turmas.html", ranking_turmas=ranking_turmas_dados, **contexto_usuario("aluno"))


@aluno_bp.route("/aluno/ranking-dos-alunos", endpoint="ranking_alunos")
@login_required("aluno")
def ranking_alunos():
    return render_template("Ranking-alunos.html", **contexto_usuario("aluno"))


@aluno_bp.route("/aluno/ranking-da-turma", endpoint="ranking_turma")
@login_required("aluno")
def ranking_turma():
    return render_template("Aluno-ranking-turma.html", **contexto_usuario("aluno"))


@aluno_bp.route("/aluno/presenca-nas-aulas", endpoint="aluno_presenca")
@login_required("aluno")
def aluno_presenca():
    boletim = db.obter_boletim(session.get("usuario_id"))
    presencas = boletim["presencas"] if boletim else []
    return render_template("Aluno-presença.html", presencas=presencas, **contexto_usuario("aluno"))
