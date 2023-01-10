from flask import render_template, request, redirect, session, flash, url_for, send_file
from app import app, db
from models import Lancamentos, Intervalos, Despesas, Usuarios, present_time, Lancamentos_query, Clientes, Motivos, Tipos_despesa, Despesas_Query
from sqlalchemy import func, text
from jsintegration.JasperServerIntegration import JasperServerIntegration
from io import BytesIO
from permissoes import permissoes
from aprovador import aprovador
from flask_mail import Message
from config_email import mail
import os

#pagina inicial com tabela dos registros
@app.route('/')
@app.route('/reemb_adian')
def index_Reembolso_Adiantamento():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    nome_usuario = Usuarios.query.filter_by(login=session['usuario_logado']).first()
    
    permissions = {}
    permissions = permissoes(permissions)

    aprovadores = {}
    aprovadores = aprovador(aprovadores)

    if 'S' in aprovadores[nome_usuario.login]:
        query = text(f'''SELECT t1.*, 
                            (select sum(t2.valor_total) from app_admin.despesas t2 where t2.id_lancamento = t1.id) as valor_total,
                            t2.nome_fantasia, t3.descricao as descricao_motivo
                            FROM app_admin.lancamentos t1
                            inner join app_admin.clientes t2 on t2.id = t1.cliente
                            inner join app_admin.motivos t3 on t3.id = t1.motivo
                            ORDER BY id
                            ''')
        lista = Lancamentos_query.query.from_statement(query).all()
    else:
        query = text(f'''SELECT t1.*, 
                (select sum(t2.valor_total) from app_admin.despesas t2 where t2.id_lancamento = t1.id) as valor_total,
                t2.nome_fantasia, t3.descricao as descricao_motivo
                FROM app_admin.lancamentos t1 
                inner join app_admin.clientes t2 on t2.id = t1.cliente
                inner join app_admin.motivos t3 on t3.id = t1.motivo
                where t1.atendente = '{nome_usuario.nome}' ORDER BY id''')
        lista = Lancamentos_query.query.from_statement(query).all()

    return render_template('index-Reembolso-Adiantamento.html', user_session = nome_usuario.nome, atendimentos_lis = lista, current_user=nome_usuario.login, permissions=permissions)

#redirecionamento para inserir novo registro
@app.route('/reemb_adian/novo')
def novo_reemb_adian():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    permissions = {}
    permissions = permissoes(permissions)
    atendentes  = Usuarios.query.filter_by(atendente="S").all()
    motivos  = Motivos.query.filter_by(ativo="S").all()
    nome_usuario = Usuarios.query.filter_by(login=session['usuario_logado']).first()
    lista_clientes = Clientes.query.all()
    return render_template('Reembolso-Adiantamento.html', user_session = nome_usuario.nome, current_user=nome_usuario.login, permissions = permissions, atendentes =atendentes,
    lista_clientes=lista_clientes, motivos = motivos)

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

    aprovadores = {}
    aprovadores = aprovador(aprovadores)

    navpills = navpills
    reg_insert_1 = reg_insert
    reg_insert = Lancamentos.query.filter_by(id=reg_insert_1).first()
    intervalos = Intervalos.query.filter_by(id_lancamento=reg_insert_1).order_by(Intervalos.id)
    query = text(f'''select t1.*, t2.descricao from 
                        app_admin.despesas t1
                        inner join app_admin.tipos_despesa t2 on t2.id = t1.tipo
                        where t1.id_lancamento = {reg_insert_1}''')
    despesas = Despesas_Query.query.from_statement(query).all()
    nome_usuario = Usuarios.query.filter_by(login=session['usuario_logado']).first()
    despesas_total = 0
    for despesa in despesas:
        despesas_total = despesas_total + despesa.valor_total
    despesas_total = despesas_total
    atendentes  = Usuarios.query.filter_by(atendente="S").all()
    motivos  = Motivos.query.filter_by(ativo="S").all()
    tipos_despesa  = Tipos_despesa.query.filter_by(ativo="S").all()
    lista_clientes = Clientes.query.all()
    return render_template('edita_Reembolso-Adiantamento.html', user_session=nome_usuario.nome, reg_insert = reg_insert, intervalos = intervalos, 
    despesas = despesas, despesas_total = despesas_total, navpills = navpills, current_user=nome_usuario.login, permissions = permissions, atendentes = atendentes,
    lista_clientes = lista_clientes, motivos = motivos, tipos_despesa = tipos_despesa, aprovadores = aprovadores)

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


@app.route('/env_aprovacao/<int:id>', methods=['GET', 'POST'])
def env_aprovacao(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
        
    env_aprovacao = Lancamentos.query.filter_by(id=id).first()
    env_aprovacao.status = "Enviado"

    msg = Message(subject='Reembolsa - Envio para Aprovação', recipients=['icaro.graciano@gmail.com'], body=f'RDV {id} enviado para aprovação',
    sender='nao.responda.reembolsa@gmail.com' )
    # Anexar um único arquivo
    with app.open_resource('report.pdf') as fp:
        msg.attach('report.pdf', 'application/pdf', fp.read())

    # Definir o caminho da pasta que contém os arquivos a serem anexados
    folder_path = 'C:/inetpub/wwwroot/Projeto Administrativo/app/static/uploads'

    #lista de arquivos a serem anexados (comprovantes de despesas)
    file_list  = Despesas.query.filter_by(id_lancamento=id).all()

    for file in file_list:
        file_path = os.path.join(folder_path, file.nome_arquivo)
        if os.path.exists(file_path):
            try:
                with open(file_path, 'rb') as fp:
                    file_content = fp.read()
                msg.attach(file.nome_arquivo, 'application/pdf', file_content)
                print(f'Arquivo {file.nome_arquivo} anexado com sucesso')
            except Exception as e:
                print(f'Erro ao anexar o arquivo {file.nome_arquivo}: {e}')
        else:
            print(f'O arquivo {file.nome_arquivo} não foi encontrado na pasta {folder_path}')

    mail.send(msg)
    db.session.add(env_aprovacao)
    db.session.commit()
    flash('Registro enviado com sucesso!')
    return redirect(url_for('edita_reemb_adian', reg_insert = env_aprovacao.id, navpills = 'navpills_2'))
