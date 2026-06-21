from flask import Flask , render_template, redirect, request, flash, send_from_directory, session as flask_session
import mysql.connector
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

app = Flask(__name__)

app.config["SECRET_KEY"] = "EUSOUALUNOLICEU"

logado = False

engine = create_engine()
Session =sessionmaker()
Base = declarative_base()
db_session = Session()

class Usuario(Base):
    __tablename__ = 'usuarios'

@app.route("/")
def login():
    if flask_session.get('logado') == True:
        if flask_session.get('tipo_usuario') == 'professor':
            return redirect('/professor/inicio')
        elif flask_session.get('tipo_usuario') == 'aluno':
            return redirect('/aluno/inicio')
    return render_template('login.html')

@app.route('/home')

@app.route('/login', methods=['POST'])
def login():

    cpf_input = request.form.get("cpf")
    senha_input = request.form.get("senha") 

    try:
        usuario = db_session.query(Usuario).filter_by(cpf=cpf_input, line=senha_input).first() 

        if usuario:
            flask_session['nome'] = usuario.nome
            flask_session['logado'] = True
            flask_session['tipo_usuario'] = usuario.tipo
        
            if usuario.tipo == 'professor':
                return redirect('/professor/inicio')
            
            if usuario.tipo == 'aluno':
                return redirect('/aluno/inicio')
        else:
            flash('Usuario ou senha invalido')
            return redirect('/')
    finally:
        db_session.close()


#-------------PROFESSOR-------------


@app.route('/professor/inicio')
def professor_inicio():
    if not flask_session.get('logado') or flask_session.get('tipo_usuario') != 'professor':
        return redirect('/')
    return render_template('tela inicial.html', nome=flask_session.get('nome'))

@app.route('/professor/lancar-notas')
def lancar_notas():
    if not flask_session.get('logado') or flask_session.get('tipo_usuario') != 'professor':
        return redirect('/')
    return render_template('.html')

@app.route('/professor/Desempenho-das-Turmas')
def Desempenho_das_Turmas():
    if not flask_session.get('logado') or flask_session.get('tipo_usuario') != 'professor':
        return redirect('/')
    return render_template('.html')

@app.route('/professor/chamadas')
def fazer_chamada():
    if not flask_session.get('logado') or flask_session.get('tipo_usuario') != 'professor':
        return redirect('/')
    return render_template('.html')

@app.route('/professor/Alunos-em-Alerta')
def Alunos_em_Alerta():
    if not flask_session.get('logado') or flask_session.get('tipo_usuario') != 'professor':
        return redirect('/')
    return render_template('.html')

@app.route('/professor/Relatorios')
def fazer_Relatorios():
    if not flask_session.get('logado') or flask_session.get('tipo_usuario') != 'professor':
        return redirect('/')
    return render_template('.html')


#-------------ALUNO-------------


@app.route('/aluno/inicio')
def aluno_inicio():
    if not flask_session.get('logado') or flask_session.get('tipo_usuario') != 'aluno':
        return redirect('/')
    return render_template('.html', nome=flask_session.get('nome'))

@app.route('/aluno/ver-notas')
def aluno_ver_notas():
    if not flask_session.get('logado') or flask_session.get('tipo_usuario') != 'aluno':
        return redirect('/')
    return render_template('.html')

@app.route('/aluno/Ranking-das-Turmas')
def Ranking_das_Turmas():
    if not flask_session.get('logado') or flask_session.get('tipo_usuario') != 'aluno':
        return redirect('/')
    return render_template('.html')

@app.route('/aluno/Ranking-dos-Alunos')
def Ranking_dos_Alunos():
    if not flask_session.get('logado') or flask_session.get('tipo_usuario') != 'aluno':
        return redirect('/')
    return render_template('.html')

@app.route('/aluno/Ranking-da-Turma')
def Ranking_da_Turma():
    if not flask_session.get('logado') or flask_session.get('tipo_usuario') != 'aluno':
        return redirect('/')
    return render_template('.html')

@app.route('/aluno/Presença-nas-Aulas')
def Presença_nas_Aulas():
    if not flask_session.get('logado') or flask_session.get('tipo_usuario') != 'aluno':
        return redirect('/')
    return render_template('.html')

@app.route('/sair')
def logout():
    flask_session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
