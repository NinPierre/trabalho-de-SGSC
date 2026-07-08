from flask import render_template, request, redirect, url_for, flash
from datetime import datetime
from database import db
from models import Professor, PresencaProfessor

@app.route('/fazer-chamada', methods=['GET', 'POST'])
def fazer_chamada():
    # DATA ATUAL DA CHAMADA (ou pega do form se houver)
    data_hoje = datetime.utcnow().date()

    if request.method == 'POST':
        try:
            # Recebe a lista de IDs de todos os alunos marcados como PRESENTES
            # No HTML, apenas os checkboxes marcados enviam o valor
            alunos_presentes_ids = request.form.getlist('presentes')
            
            # Pega todos os alunos cadastrados no banco
            todos_alunos = aluno.query.all()

            for aluno in todos_alunos:
                # Se o ID do aluno está na lista do form, ele veio presente
                esta_presente = str(aluno.id) in alunos_presentes_ids
                
                # Pega a observação individual (ex: obs_1, obs_2)
                obs = request.form.get(f'obs_{aluno.id}', '')

                # Verifica se já existe chamada deste aluno na data de hoje
                presenca = PresencaAluno.query.filter_by(
                    aluno_id=aluno.id,
                    data=data_hoje
                ).first()

                if presenca:
                    # Atualiza chamada existente
                    presenca.presente = esta_presente
                    presenca.observacao = obs
                else:
                    # Cria um novo registro
                    nova_presenca = PresencaAluno(
                        aluno_id=aluno.id,
                        data=data_hoje,
                        presente=esta_presente,
                        observacao=obs
                    )
                    db.session.add(nova_presenca)

            db.session.commit()
            flash('Chamada salva com sucesso!', 'success')
            return redirect(url_for('fazer_chamada'))

        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao salvar chamada: {str(e)}', 'danger')

    # GET: Busca todos os alunos para listar na tela
    alunos = aluno.query.all()
    return render_template('chamada.html', alunos=alunos, data_hoje=data_hoje)











                    #professor/inicio
                    from flask import render_template, redirect, url_for, flash
from datetime import datetime
from database import db
from models import Professor, Turma, PresencaProfessor  # Ajuste os imports para os seus models

@app.route("/professor/inicio")
@login_required("professor")
def professor_inicio():
    # 1. Recupera o contexto padrão do usuário (nome, foto, etc.)
    contexto = contexto_usuario("professor")
    
    # Supondo que o contexto_usuario retorne o ID ou objeto do professor logado:
    # Caso não venha, você pode pegar pela sessão (ex: session.get('user_id'))
    professor_id = contexto.get("usuario_id")  

    data_hoje = datetime.utcnow().date()

    # 2. Busca as turmas/disciplinas associadas a este professor
    turmas = Turma.query.filter_by(professor_id=professor_id).all()

    # 3. Verifica o status da presença do próprio professor no dia de hoje
    presenca_hoje = PresencaProfessor.query.filter_by(
        professor_id=professor_id, 
        data=data_hoje
    ).first()

    # 4. Adiciona as informações específicas da tela inicial ao dicionário de contexto
    contexto.update({
        "turmas": turmas,
        "presenca_hoje": presenca_hoje,
        "data_hoje": data_hoje.strftime('%d/%m/%Y'),
        "total_turmas": len(turmas)
    })

    # 5. Renderiza o template passando o contexto desempacotado
    return render_template("Professor-inical.html", **contexto)










                  #professor/lancar notas
                  from flask import request, render_template, redirect, url_for, flash

@app.route("/professor/lancar-notas", methods=["GET", "POST"])
@login_required("professor")
def lancar_notas():
    # 1. Recupera o contexto do usuário (ex: ID do professor logado)
    contexto = contexto_usuario("professor")
    id_professor = contexto.get("usuario_id") # Ajuste a chave conforme sua estrutura
    
    if request.method == "POST":
        # 2. Recebe os dados enviados pelo formulário HTML
        # O formulário pode enviar uma lista de alunos e suas respectivas notas
        aluno_ids = request.form.getlist("aluno_id[]")
        notas = request.form.getlist("nota[]")
        id_disciplina = request.form.get("disciplina_id")
        id_turma = request.form.get("turma_id")
        
        try:
            # 3. Salva as notas no banco de dados
            for id_aluno, nota in zip(aluno_ids, notas):
                if nota: # Verifica se a nota não está em branco
                    # EXEMPLO com SQL Puro (ajuste para seu ORM como SQLAlchemy se necessário):
                    # db.execute("""
                    #     INSERT INTO notas (aluno_id, disciplina_id, turma_id, nota) 
                    #     VALUES (%s, %s, %s, %s)
                    #     ON CONFLICT (aluno_id, disciplina_id) DO UPDATE SET nota = EXCLUDED.nota
                    # """, (id_aluno, id_disciplina, id_turma, float(nota)))
                    pass
            
            flash("Notas lançadas com sucesso!", "success")
            return redirect(url_for("lancar_notas"))
            
        except Exception as e:
            flash(f"Erro ao salvar as notas: {str(e)}", "danger")
    
    # --- Requisição GET ---
    # 4. Busca os dados necessários para preencher os selects/tabelas do HTML
    # (Exemplo: listar as turmas e disciplinas que este professor leciona)
    # turmas = buscar_turmas_do_professor(id_professor)
    # contexto["turmas"] = turmas

    return render_template("Professor-lancar-notas.html", **contexto)













                 #profesor/desempenho das turmas
                 from flask import render_template, request, flash
# Importe seu objeto de banco de dados ou modelos aqui (ex: de models import Turma, Nota, Aluno)

@app.route("/professor/desempenho-das-turmas")
@login_required("professor")
def professor_desempenho():
    # 1. Recupera o contexto básico do usuário (nome, cargo, etc.)
    contexto = contexto_usuario("professor")
    id_professor = contexto.get("usuario_id") # Ajuste a chave conforme seu sistema
    
    # 2. Captura filtros opcionais vindos da URL (ex: se o professor filtrar por uma turma específica)
    id_turma_selecionada = request.args.get("turma_id")
    
    try:
        # 3. Lógica para buscar as turmas que este professor leciona
        # (Substitua pela sua lógica de banco de dados/ORM)
        # turmas = db.session.query(Turma).filter_by(professor_id=id_professor).all()
        # contexto["turmas"] = turmas
        
        # 4. Cálculo das métricas de desempenho
        desempenho_turmas = []
        
        # EXEMPLO de estrutura de dados que o seu HTML vai precisar para gerar os gráficos/tabelas:
        # Se houver um filtro de turma, você pode focar em uma, caso contrário, calcula de todas
        
        # para cada turma em turmas:
        #     media_turma = calcular_media_da_turma(turma.id)
        #     aprovados = contar_aprovados(turma.id)
        #     reprovados = contar_reprovados(turma.id)
        #     
        #     desempenho_turmas.append({
        #         "nome_turma": turma.nome,
        #         "disciplina": turma.disciplina,
        #         "media_geral": media_turma,
        #         "taxa_aprovacao": (aprovados / (aprovados + reprovados)) * 100 if (aprovados + reprovados) > 0 else 0,
        #         "total_alunos": aprovados + reprovados
        #     })
        
        # Dados fictícios para o funcionamento inicial do template:
        contexto["desempenho_turmas"] = [
            {"nome_turma": "3º Ano A", "disciplina": "Matemática", "media_geral": 7.5, "taxa_aprovacao": 85, "total_alunos": 30},
            {"nome_turma": "2º Ano B", "disciplina": "Física", "media_geral": 6.2, "taxa_aprovacao": 70, "total_alunos": 25}
        ]
        
        if id_turma_selecionada:
            contexto["turma_filtrada"] = id_turma_selecionada
            
    except Exception as e:
        flash(f"Erro ao carregar dados de desempenho: {str(e)}", "danger")
        contexto["desempenho_turmas"] = []

    # 5. Renderiza o template passando o contexto enriquecido com os dados de desempenho
    return render_template("Professor-desempenho.html", **contexto)










                          #professor/chamadas
from flask import request, render_template, redirect, url_for, flash
from datetime import date # Para pegar a data atual automaticamente

@app.route("/professor/chamadas", methods=["GET", "POST"])
@login_required("professor")
def fazer_chamada():
    # 1. Recupera o contexto do professor logado
    contexto = contexto_usuario("professor")
    id_professor = contexto.get("usuario_id")
    
    # 2. Captura filtros vindos da URL (Ex: após o professor escolher a turma e a disciplina)
    id_turma = request.args.get("turma_id")
    id_disciplina = request.args.get("disciplina_id")
    data_chamada = request.args.get("data", date.today().strftime("%Y-%m-%d"))
    
    # Injeta os filtros de volta no contexto para manter a tela preenchida
    contexto["turma_id_selecionada"] = id_turma
    contexto["disciplina_id_selecionada"] = id_disciplina
    contexto["data_chamada"] = data_chamada

    if request.method == "POST":
        # Recebe os dados enviados pelo formulário
        id_turma_post = request.form.get("turma_id")
        id_disciplina_post = request.form.get("disciplina_id")
        data_post = request.form.get("data_chamada")
        
        # O truque aqui é pegar a lista de TODOS os alunos listados na tela
        alunos_ids = request.form.getlist("aluno_id[]")
        # E pegar apenas os IDs dos alunos que foram marcados como PRESENTE (via checkbox)
        presencas = request.form.getlist("presenca[]") 
        
        try:
            # 3. Salva no Banco de Dados
            for id_aluno in alunos_ids:
                # Se o ID do aluno está na lista de presenças, status é 'P', senão 'F'
                status = "P" if id_aluno in presencas else "F"
                
                # EXEMPLO DE SQL (Ajuste para o seu banco ou ORM):
                # db.execute("""
                #     INSERT INTO frequencias (aluno_id, turma_id, disciplina_id, data, status)
                #     VALUES (%s, %s, %s, %s, %s)
                #     ON CONFLICT (aluno_id, data, disciplina_id) DO UPDATE SET status = EXCLUDED.status
                # """, (id_aluno, id_turma_post, id_disciplina_post, data_post, status))
                pass
                
            flash("Chamada salva com sucesso!", "success")
            # Redireciona mantendo os filtros para o professor ver que foi salvo
            return redirect(url_for("fazer_chamada", turma_id=id_turma_post, disciplina_id=id_disciplina_post, data=data_post))
            
        except Exception as e:
            flash(f"Erro ao salvar a chamada: {str(e)}", "danger")

    # --- Requisição GET ---
    # 4. Busca turmas/disciplinas do professor para montar os selects do filtro
    # contexto["turmas"] = buscar_turmas_do_professor(id_professor)
    
    # 5. Se o professor já selecionou uma turma, busca a lista de alunos dela
    if id_turma:
        # contexto["alunos"] = buscar_alunos_da_turma(id_turma)
        # Exemplo de estrutura que o HTML espera receber em contexto["alunos"]:
        contexto["alunos"] = [
            {"id": "1", "nome": "Ana Silva"},
            {"id": "2", "nome": "Bruno Costa"},
            {"id": "3", "nome": "Carlos Souza"}
        ]
    else:
        contexto["alunos"] = []

    return render_template("Professor-chamadas.html", **contexto)










              #professor/alunos em alerta

from flask import render_template, request, flash

@app.route("/professor/alunos-em-alerta")
@login_required("professor")
def alunos_alerta():
    # 1. Recupera o contexto básico do professor
    contexto = contexto_usuario("professor")
    id_professor = contexto.get("usuario_id")
    
    # 2. Captura filtros opcionais da URL (caso queira filtrar alertas por turma)
    id_turma_selecionada = request.args.get("turma_id")
    contexto["turma_id_selecionada"] = id_turma_selecionada

    try:
        # 3. Busca as turmas do professor para popular o filtro na tela
        # contexto["turmas"] = buscar_turmas_do_professor(id_professor)
        
        # 4. Lógica para buscar os alunos em situação de risco (Notas Baixas ou Faltas Altas)
        # (Substitua a estrutura abaixo pelas consultas reais ao seu banco de dados)
        
        # Exemplo de dados estruturados que o seu HTML 'Professor-alertas.html' vai precisar:
        alertas_alunos = [
            {
                "nome": "Ana Silva",
                "turma": "3º Ano A",
                "disciplina": "Matemática",
                "motivo": "Nota Abaixo da Média",
                "detalhe": "Média atual: 4.5 (Mínima: 6.0)",
                "nivel_critico": "perigo" # Usado para estilização CSS (ex: badge vermelho)
            },
            {
                "nome": "Bruno Costa",
                "turma": "3º Ano A",
                "disciplina": "Matemática",
                "motivo": "Excesso de Faltas",
                "detalhe": "Frequência: 72% (Mínima: 75%)",
                "nivel_critico": "atencao" # Usado para estilização CSS (ex: badge amarelo)
            }
        ]
        
        # Se o professor escolheu uma turma no filtro, filtramos a lista
        if id_turma_selecionada:
            # Em produção, você faria esse filtro direto na sua query SQL/ORM
            # exemplo: WHERE turma_id = id_turma_selecionada
            pass
            
        contexto["alertas"] = alertas_alunos
        
    except Exception as e:
        flash(f"Erro ao carregar a lista de alertas: {str(e)}", "danger")
        contexto["alertas"] = []

    # 5. Renderiza a página com a lista de alunos em risco
    return render_template("Professor-alertas.html", **contexto)










                             #professor/relatorios
                             from flask import render_template, request, flash, send_file
import io # Utilizado caso você queira gerar arquivos na memória para download

@app.route("/professor/relatorios", methods=["GET", "POST"])
@login_required("professor")
def professor_relatorios():
    # 1. Recupera o contexto do professor logado
    contexto = contexto_usuario("professor")
    id_professor = contexto.get("usuario_id")
    
    # 2. Captura os filtros que o professor selecionou na tela
    id_turma = request.args.get("turma_id")
    id_disciplina = request.args.get("disciplina_id")
    tipo_relatorio = request.args.get("tipo_relatorio") # ex: 'notas', 'frequencia', 'historico'
    
    # Devolve os filtros para manter a tela preenchida
    contexto["turma_selecionada"] = id_turma
    contexto["disciplina_selecionada"] = id_disciplina
    contexto["tipo_relatorio_selecionado"] = tipo_relatorio

    try:
        # 3. Busca turmas e disciplinas para preencher os menus do filtro
        # contexto["turmas"] = buscar_turmas_do_professor(id_professor)
        
        # 4. Se o professor enviou uma requisição POST ou clicou em "Baixar", 
        # você pode processar o download do arquivo (PDF / Excel)
        if request.method == "POST" or request.args.get("download") == "true":
            # Aqui entraria a lógica de bibliotecas como ReportLab (PDF) ou OpenPyXL (Excel)
            # exemplo_arquivo = gerar_pdf_relatorio(id_turma, id_disciplina, tipo_relatorio)
            # return send_file(exemplo_arquivo, as_attachment=True, download_name="relatorio.pdf")
            
            flash("Download do relatório iniciado!", "success")
            
        # 5. Se for apenas uma visualização em tela (GET com filtros aplicados)
        elif id_turma and tipo_relatorio:
            # Busca os dados no banco para exibir uma prévia na tabela do HTML
            # dados_relatorio = buscar_dados_para_relatorio(id_turma, id_disciplina, tipo_relatorio)
            
            # Exemplo de estrutura de dados para o HTML renderizar a prévia:
            contexto["dados_preview"] = {
                "cabecalho": ["Aluno", "Média Parcial", "Faltas", "Situação"],
                "linhas": [
                    ["Ana Silva", "8.5", "2", "Aprovado"],
                    ["Bruno Costa", "5.0", "12", "Recuperação"],
                    ["Carlos Souza", "7.0", "4", "Aprovado"]
                ]
            }
        else:
            contexto["dados_preview"] = None

    except Exception as e:
        flash(f"Erro ao processar ou gerar o relatório: {str(e)}", "danger")
        contexto["dados_preview"] = None

    # 6. Renderiza a página de relatórios
    return render_template("Professor-relatorios.html", **contexto)











                     #aluno/inicio
                     from flask import render_template, flash
from datetime import date # Para filtrar o horário pelo dia da semana atual

@app.route("/aluno/inicio")
@login_required("aluno")
def aluno_inicio():
    # 1. Recupera o contexto básico do aluno logado (nome, matrícula, etc.)
    contexto = contexto_usuario("aluno")
    id_aluno = contexto.get("usuario_id") # Ajuste para a chave que você usa no sistema
    
    try:
        # 2. Busca avisos ou notificações recentes da escola/faculdade
        # contexto["avisos"] = buscar_avisos_recentes()
        contexto["avisos"] = [
            {"titulo": "Período de Provas", "conteudo": "As avaliações do 2º bimestre começam na próxima semana.", "data": "08/07/2026"},
            {"titulo": "Feira de Ciências", "conteudo": "Inscrições prorrogadas até sexta-feira.", "data": "06/07/2026"}
        ]
        
        # 3. Busca o horário das aulas do aluno para o dia de hoje
        dia_da_semana = date.today().weekday() # Retorna 0 para segunda, 1 para terça, etc.
        # contexto["aulas_hoje"] = buscar_horario_aluno(id_aluno, dia_da_semana)
        contexto["aulas_hoje"] = [
            {"horario": "07:30 - 09:10", "disciplina": "Matemática", "sala": "Bloco A - Sala 4"},
            {"horario": "09:30 - 11:10", "disciplina": "Física", "sala": "Laboratório 2"}
        ]
        
        # 4. Busca um resumo do desempenho do aluno (ex: média geral e frequência acumulada)
        # contexto["resumo_desempenho"] = calcular_resumo_aluno(id_aluno)
        contexto["resumo_desempenho"] = {
            "media_geral": 7.8,
            "frequencia_total": 88.5, # Em porcentagem
            "alertas_pendentes": 0
        }
        
    except Exception as e:
        flash(f"Erro ao carregar o painel do aluno: {str(e)}", "danger")
        # Garante que as variáveis existam no HTML mesmo se o banco falhar
        contexto["avisos"] = []
        contexto["aulas_hoje"] = []
        contexto["resumo_desempenho"] = {"media_geral": "-", "frequencia_total": "-", "alertas_pendentes": 0}

    # 5. Renderiza a página passando todo o painel montado
    return render_template("Aluno-inicial.html", **contexto)








                  
                  
                  
                  
                  #aluno/ver notas
                  from flask import render_template, flash

@app.route("/aluno/ver-notas")
@login_required("aluno")
def aluno_notas():
    # 1. Recupera o contexto do aluno logado (nome, matrícula, etc.)
    contexto = contexto_usuario("aluno")
    id_aluno = contexto.get("usuario_id") # Ajuste conforme a chave do seu sistema
    
    try:
        # 2. Busca as notas do aluno no banco de dados agrupadas por disciplina
        # (Substitua a estrutura mockada abaixo pela sua query real do Banco/ORM)
        # notas_aluno = buscar_boletim_completo_do_aluno(id_aluno)
        
        notas_aluno = [
            {
                "disciplina": "Matemática",
                "n1": 7.5,
                "n2": 8.0,
                "n3": 6.5,
                "n4": 7.0,
                "media_final": 7.25,
                "situacao": "Aprovado"
            },
            {
                "disciplina": "Física",
                "n1": 5.0,
                "n2": 4.5,
                "n3": 6.0,
                "n4": 5.5,
                "media_final": 5.25,
                "situacao": "Recuperação"
            },
            {
                "disciplina": "História",
                "n1": 9.0,
                "n2": 8.5,
                "n3": 9.5,
                "n4": 10.0,
                "media_final": 9.25,
                "situacao": "Aprovado"
            }
        ]
        
    except Exception as e:
        flash(f"Erro ao carregar o boletim: {str(e)}", "danger")
        notas_aluno = []

    # 3. Renderiza o template passando o dicionário de contexto + a lista de notas
    return render_template("Aluno-notas.html", notas=notas_aluno, **contexto)
                    










                    #aluno/ranking das turmas
                    from flask import render_template, flash

@app.route("/aluno/ranking-das-turmas")
@login_required("aluno")
def ranking_turmas():
    # 1. Recupera o contexto do aluno logado
    contexto = contexto_usuario("aluno")
    id_aluno = contexto.get("usuario_id")
    
    try:
        # 2. Busca o ranking geral das turmas ordenado pela maior média/pontuação
        # (Substitua pelos dados dinâmicos do seu banco ou ORM no futuro)
        # lista_ranking = buscar_ranking_geral_das_turmas()
        
        lista_ranking = [
            {"posicao": 1, "nome_turma": "3º Ano A - Informática", "pontuacao": 8.7, "destaque": "Melhor Média em Exatas"},
            {"posicao": 2, "nome_turma": "2º Ano B - Alimentos", "pontuacao": 8.2, "destaque": "Maior Frequência Geral"},
            {"posicao": 3, "nome_turma": "1º Ano A - Química", "pontuacao": 7.9, "destaque": "Evolução do Mês"},
            {"posicao": 4, "nome_turma": "3º Ano B - Administração", "pontuacao": 7.4, "destaque": "-"},
        ]
        
        # 3. Opcional: Identificar qual é a turma específica deste aluno logado 
        # para destacá-la visualmente no ranking
        # id_turma_do_aluno = buscar_turma_do_aluno(id_aluno)
        # contexto["minha_turma_nome"] = "3º Ano A - Informática"  # Exemplo
        
    except Exception as e:
        flash(f"Erro ao carregar o ranking das turmas: {str(e)}", "danger")
        lista_ranking = []

    # 4. Renderiza o template enviando a lista ordenada
    return render_template("Ranking-turmas.html", ranking_turmas=lista_ranking, **contexto)










                    #aluno/ranking dos alunos
                    from flask import render_template, flash

@app.route("/aluno/ranking-dos-alunos")
@login_required("aluno")
def ranking_alunos():
    # 1. Recupera o contexto do aluno logado (incluindo o ID e o Nome)
    contexto = contexto_usuario("aluno")
    id_aluno_logado = contexto.get("usuario_id")
    
    try:
        # 2. Busca os dados de classificação dos alunos
        # Em produção, você faria uma query ordenando por nota decrescente
        # exemplo: db.session.query(Aluno).order_by(Aluno.media.desc()).all()
        
        lista_ranking = [
            {"posicao": 1, "nome": "História", "aluno": "Ana Silva", "pontuacao": 9.8, "id": "101"},
            {"posicao": 2, "nome": "História", "aluno": "Carlos Souza", "pontuacao": 9.5, "id": "102"},
            {"posicao": 3, "nome": "História", "aluno": "Mariana Lima", "pontuacao": 9.2, "id": "103"},
            {"posicao": 4, "nome": "História", "aluno": "Beatriz Reis", "pontuacao": 8.9, "id": "104"},
            # Supondo que este seja o aluno logado na simulação:
            {"posicao": 5, "nome": "História", "aluno": contexto.get("nome_usuario", "Seu Nome"), "pontuacao": 8.5, "id": id_aluno_logado}
        ]
        
        # 3. Identifica a posição exata do aluno logado para exibir um destaque no topo da tela
        seu_posicionamento = next((item for item in lista_ranking if item["id"] == id_aluno_logado), None)
        contexto["seu_posicionamento"] = seu_posicionamento

    except Exception as e:
        flash(f"Erro ao carregar o ranking de alunos: {str(e)}", "danger")
        lista_ranking = []
        contexto["seu_posicionamento"] = None

    # 4. Envia a lista tratada para o template HTML
    return render_template("Ranking-alunos.html", ranking_alunos=lista_ranking, **contexto)














                         #aluno/ranking da turma
                         from flask import render_template, flash

@app.route("/aluno/ranking-da-turma")
@login_required("aluno")
def ranking_turma():
    # 1. Recupera o contexto do aluno logado (incluindo o ID do usuário)
    contexto = contexto_usuario("aluno")
    id_aluno_logado = contexto.get("usuario_id")
    
    try:
        # 2. Busca a turma à qual este aluno pertence
        # id_turma_aluno = buscar_turma_do_aluno(id_aluno_logado)
        # contexto["nome_turma"] = "3º Ano A - Informática"  # Exemplo de meta-dado
        
        # 3. Busca o ranking filtrando apenas pelos alunos daquela turma específica
        # Em produção, sua query seria parecida com:
        # db.session.query(Aluno).filter_by(turma_id=id_turma_aluno).order_by(Aluno.media.desc()).all()
        
        lista_ranking_turma = [
            {"posicao": 1, "aluno": "Ana Silva", "pontuacao": 9.8, "id": "101"},
            {"posicao": 2, "aluno": "Carlos Souza", "pontuacao": 9.5, "id": "102"},
            # Supondo que este seja o aluno logado:
            {"posicao": 3, "aluno": contexto.get("nome_usuario", "Seu Nome"), "pontuacao": 8.5, "id": id_aluno_logado},
            {"posicao": 4, "aluno": "Mariana Lima", "pontuacao": 8.2, "id": "103"},
            {"posicao": 5, "aluno": "Pedro Rocha", "pontuacao": 7.9, "id": "105"}
        ]
        
        # 4. Encontra a posição do próprio aluno para destacar na interface
        sua_posicao = next((item["posicao"] for item in lista_ranking_turma if item["id"] == id_aluno_logado), None)
        contexto["sua_posicao_turma"] = sua_posicao

    except Exception as e:
        flash(f"Erro ao carregar o ranking da turma: {str(e)}", "danger")
        lista_ranking_turma = []
        contexto["sua_posicao_turma"] = None

    # 5. Envia os dados filtrados para o template
    return render_template("Aluno-ranking-turma.html", ranking_turma=lista_ranking_turma, **contexto)














                          #aluno/presenca nas aulas
                          from flask import render_template, flash

@app.route("/aluno/presenca-nas-aulas")
@login_required("aluno")
def aluno_presenca():
    # 1. Recupera o contexto do aluno logado
    contexto = contexto_usuario("aluno")
    id_aluno = contexto.get("usuario_id") # Ajuste conforme a chave do seu sistema
    
    try:
        # 2. Busca o resumo de faltas e presenças por disciplina
        # (Substitua pelos dados dinâmicos do seu banco ou ORM no futuro)
        # frequencia_dados = buscar_frequencia_detalhada_aluno(id_aluno)
        
        frequencia_dados = [
            {
                "disciplina": "Matemática",
                "aulas_dadas": 40,
                "presencas": 36,
                "faltas": 4,
                "porcentagem": 90.0,
                "situacao": "Regular"
            },
            {
                "disciplina": "Física",
                "aulas_dadas": 40,
                "presencas": 28,
                "faltas": 12,
                "porcentagem": 70.0,
                "situacao": "Alerta" # Abaixo dos 75% exigidos por lei
            },
            {
                "disciplina": "História",
                "aulas_dadas": 30,
                "presencas": 30,
                "faltas": 0,
                "porcentagem": 100.0,
                "situacao": "Regular"
            }
        ]
        
        # 3. Calcula os totais gerais para exibir em blocos de destaque (cards)
        total_aulas = sum(d["aulas_dadas"] for d in frequencia_dados)
        total_faltas = sum(d["faltas"] for d in frequencia_dados)
        
        if total_aulas > 0:
            porcentagem_geral = ((total_aulas - total_faltas) / total_aulas) * 100
        else:
            porcentagem_geral = 100.0

        # Injeta os indicadores gerais no contexto
        contexto["frequencia_geral"] = round(porcentagem_geral, 1)
        contexto["total_faltas"] = total_faltas
        contexto["historico_frequencia"] = frequencia_dados
        
    except Exception as e:
        flash(f"Erro ao carregar dados de presença: {str(e)}", "danger")
        contexto["frequencia_geral"] = "-"
        contexto["total_faltas"] = "-"
        contexto["historico_frequencia"] = []

    # 4. Renderiza o template com o contexto atualizado
    return render_template("Aluno-presença.html", **contexto)









                          #aluno/sair
                                from flask import session, redirect, url_for, flash

@app.route("/sair")
def logout():
    # 1. Limpa completamente o dicionário de sessão do Flask
    # Isso remove chaves como 'usuario_id', 'usuario_tipo', etc.
    session.clear()
    
    # 2. Opcional: Envia uma mensagem amigável de confirmação para a tela de login
    flash("Sessão encerrada com sucesso.", "info")
    
    # 3. Redireciona o usuário para a rota da página de login
    return redirect(url_for("login"))


# --- Inicialização do Servidor ---
# Garante que o app só vai rodar se este arquivo for executado diretamente
if __name__ == "__main__":
    # debug=True: Ativa o reinício automático do servidor ao alterar o código
    # e mostra um terminal de erros detalhado diretamente no navegador.
    app.run(debug=True)    
