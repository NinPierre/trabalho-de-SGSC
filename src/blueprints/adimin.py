from flask import Blueprint, render_template, session

import adm as db
from src.blueprints.auth import login_required

admin_bp = Blueprint("admin_bp", __name__)

def contexto_usuario(perfil):
    nome = session.get("nome") or "Usuário"
    return {"nome": nome, "nome_usuario": nome, "perfil": perfil}

@admin_bp.route("/admin/dashboard", endpoint="admin_dashboard")
@login_required("admin")
def admin_dashboard():
    return render_template("admin_dashboard.html", **contexto_usuario("admin"))
