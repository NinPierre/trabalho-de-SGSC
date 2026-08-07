from database import Base, engine
import adm as db


def limpar_cpf(cpf):
    return "".join(char for char in (cpf or "") if char.isdigit())


def autenticar_usuario(cpf, senha):
    cpf_limpo = limpar_cpf(cpf)
    try:
        return db.buscar_usuario(cpf_limpo, senha)
    except Exception as exc:
        print(f"Erro ao autenticar: {exc}")
        return None


def perfil_para_sessao(perfil):
    if perfil == "admin":
        return "admin"
    elif perfil == "professor":
        return "professor"
    return "aluno"
