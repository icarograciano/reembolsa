from flask import render_template, request, redirect, session, flash, url_for, send_file
from app import app, db
from models import Lancamentos, Intervalos, Despesas, Usuarios, present_time, Lancamentos_query 
from sqlalchemy import func, text
from jsintegration.JasperServerIntegration import JasperServerIntegration
from io import BytesIO
from permissoes import permissoes

#pagina inicial com tabela dos registros
@app.route('/')
@app.route('/reemb_adian')
def index_Reembolso_Adiantamento():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    permissions = {}
    permissions = permissoes(permissions)
    print(permissions)
    #lista = Lancamentos.query.order_by(Lancamentos.id)
    query = text('''SELECT t1.*, 
                    (select sum(t2.valor_total) from app_admin.despesas t2 where t2.id_lancamento = t1.id) as valor_total
                    FROM app_admin.lancamentos t1 ORDER BY id''')
    lista = Lancamentos_query.query.from_statement(query).all()
    nome_usuario = Usuarios.query.filter_by(login=session['usuario_logado']).first()
    print(nome_usuario.login)
    return render_template('index-Reembolso-Adiantamento.html', user_session = nome_usuario.nome, atendimentos_lis = lista, current_user=nome_usuario.login, permissions=permissions)

#redirecionamento para inserir novo registro
@app.route('/reemb_adian/novo')
def novo_reemb_adian():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    permissions = {}
    permissions = permissoes(permissions)
    nome_usuario = Usuarios.query.filter_by(login=session['usuario_logado']).first()
    return render_template('Reembolso-Adiantamento.html', user_session = nome_usuario.nome, current_user=nome_usuario.login, permissions = permissions)

#inserindo novo registro
@app.route('/reemb_adian/criar', methods=['POST',])
def criar_reemb_adian():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))

    atendimento_cliente = request.form['atendimento_cliente']
    atendimento_motivo = request.form['atendimento_motivo']
    atendimento_discriminacao = request.form['atendimento_discriminacao']
    atendimento_dt_atendimento = request.form['atendimento_dt_atendimento']
    atendimento_atendente = request.form['atendimento_atendente']
    atendimento_status = "Aberto"

    novo_lancamento = Lancamentos(cliente = atendimento_cliente, motivo = atendimento_motivo, dt_atendimento = atendimento_dt_atendimento,
    descr_atendimento = atendimento_discriminacao, atendente = atendimento_atendente, 
    status = atendimento_status, usuario_add = session['usuario_logado'] , usuario_edicao = session['usuario_logado'], 
    data_add = f'''{present_time}''' , data_edicao = f'''{present_time}''')
    
    db.session.add(novo_lancamento)
    db.session.commit()
    flash('Registro incluído com sucesso!')
    return redirect(url_for('edita_reemb_adian', reg_insert = novo_lancamento.id, navpills = 'navpills_2'))

#redirecionamento para editar novo registro
@app.route('/reemb_adian/editar/<int:reg_insert>/<navpills>',  methods=['POST','GET'])
def edita_reemb_adian(reg_insert, navpills):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    permissions = {}
    permissions = permissoes(permissions)
    navpills = navpills
    reg_insert_1 = reg_insert
    reg_insert = Lancamentos.query.filter_by(id=reg_insert_1).first()
    intervalos = Intervalos.query.filter_by(id_lancamento=reg_insert_1).order_by(Intervalos.id)
    despesas = Despesas.query.filter_by(id_lancamento=reg_insert_1).order_by(Despesas.id)
    nome_usuario = Usuarios.query.filter_by(login=session['usuario_logado']).first()
    despesas_total = 0
    for despesa in despesas:
        despesas_total = despesas_total + despesa.valor_total
    despesas_total = despesas_total
    return render_template('edita_Reembolso-Adiantamento.html', user_session=nome_usuario.nome, reg_insert = reg_insert, intervalos = intervalos, 
    despesas = despesas, despesas_total = despesas_total, navpills = navpills, current_user=nome_usuario.login, permissions = permissions)

#atualizando o registro
@app.route('/reemb_adian/atualizar', methods=['POST',])
def atualiza_reemb_adian():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    reg_insert_1 = Lancamentos.query.filter_by(id=request.form['id']).first()
    reg_insert_1.status = request.form.get('atendimento_status') if request.form.get('atendimento_status') != None else reg_insert_1.status 
    reg_insert_1.cliente = request.form.get('atendimento_cliente') if request.form.get('atendimento_cliente') != None else reg_insert_1.cliente
    reg_insert_1.motivo = request.form.get('atendimento_motivo') if request.form.get('atendimento_motivo') != None else reg_insert_1.motivo 
    reg_insert_1.dt_atendimento = request.form['atendimento_dt_atendimento']
    reg_insert_1.atendente = request.form.get('atendimento_atendente') if request.form.get('atendimento_atendente') != None else reg_insert_1.atendente 
    reg_insert_1.descr_atendimento = request.form['atendimento_discriminacao']
    reg_insert_1.data_edicao = f'''{present_time}''' 
    reg_insert_1.usuario_edicao = session['usuario_logado']

    db.session.add(reg_insert_1)
    db.session.commit()
    flash('Registro editado com sucesso!')
    return redirect(url_for('edita_reemb_adian', reg_insert = reg_insert_1.id, navpills = 'navpills_2'))

#deletando o registro
@app.route('/reemb_adian/deletar/<int:id>')
def deletar_reemb_adian(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    Lancamentos.query.filter_by(id=id).delete()
    Intervalos.query.filter_by(id_lancamento=id).delete()
    Despesas.query.filter_by(id_lancamento=id).delete()
    db.session.commit()
    flash('Registro deletado com sucesso!')

    return redirect(url_for('index_Reembolso_Adiantamento'))

#geração de relatorio 
@app.route('/rel_reemb_adian/<int:id>', methods=['GET', 'POST'])
def rel_reemb_adian(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    parameter1 = id
    obj = JasperServerIntegration(
      'http://localhost:8082/jasperserver',   # URL do Jasper Server
      'reports/Invoice',                      # Caminho para o Relatório sem a primeira barra
      'pdf',                                  # Tipo do Arquivo do Relatório
      'jasperadmin',                          # Usuário com acesso ao relatório
      'jasperadmin',                          # Senha do usuário
      {"ID" :  parameter1}                    # Parâmetros opcionais
    )
    # Obtém os bytes do relatório
    try:
      report = obj.execute()
      # Transforma os bytes do relatório em um objeto BytesIO
      report_bytesio = BytesIO(report)  
      
      # Aqui, você pode fazer o que você quiser.
      # No caso, vamos salvar o arquivo no disco, como report.pdf
    # Crie um nome de arquivo temporário para armazenar o relatório
      temp_file = 'report.pdf'
      with open(temp_file, 'wb') as f:
          f.write(report)
          # Use o método send_file para enviar o arquivo para o navegador
          return send_file(temp_file, mimetype='application/pdf')
    # Exceção, caso ocorra um erro na geração do relatório
    except:
      print('Error ' + obj.error_code + ': ' + obj.error_message)