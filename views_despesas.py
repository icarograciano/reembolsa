from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from app import app, db
from models import Despesas, Intervalos, Lancamentos, Usuarios, present_time, Tipos_despesa, Despesas_Query
import os
from werkzeug.utils import secure_filename
from permissoes import permissoes
from sqlalchemy import func, text
from aprovador import aprovador

@app.route('/despesas/criar', methods=['POST',])
def criar_despesas():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    dt_despesa = request.form['dt_despesa']
    tipo = request.form['tipo']
    quantidade = float(request.form['quantidade'])
    valor_despesa = float(str(request.form['valor_despesa']).replace(',','.'))
    valor_total = quantidade * valor_despesa
    id_lancamento = request.form['id_lancamento']
    observacao = request.form['observacao']
    anexo = 'N'
    nova_despesa = Despesas(dt_despesa = dt_despesa, tipo = tipo, quantidade = quantidade, valor_despesa = valor_despesa, id_lancamento = id_lancamento, valor_total = valor_total,
    usuario_add = session['usuario_logado'] , usuario_edicao = session['usuario_logado'], data_add = f'''{present_time}''' , data_edicao = f'''{present_time}''',
    observacao = observacao, anexo = anexo)
    db.session.add(nova_despesa)
    db.session.commit()
    flash('Despesa criada com sucesso!')
    return redirect(url_for('edita_reemb_adian', reg_insert=id_lancamento, navpills = 'navpills_4'))

@app.route('/despesas/editar/<int:id_lancamento>/<int:id>')
def editar_despesa(id_lancamento, id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    permissions = {}
    permissions = permissoes(permissions)

    aprovadores = {}
    aprovadores = aprovador(aprovadores)
    
    id_lancamento = id_lancamento
    reg_insert = Lancamentos.query.filter_by(id=id_lancamento).first()
    intervalos = Intervalos.query.filter_by(id_lancamento=id_lancamento).order_by(Intervalos.id)
    query = text(f'''select t1.*, t2.descricao from 
                        app_admin.despesas t1
                        inner join app_admin.tipos_despesa t2 on t2.id = t1.tipo
                        where t1.id_lancamento = {id_lancamento}''')
    despesas = Despesas_Query.query.from_statement(query).all()
    nome_usuario = Usuarios.query.filter_by(login=session['usuario_logado']).first()
    despesas_total = 0
    for despesa in despesas:
        despesas_total = despesas_total + despesa.valor_total
    despesas_total = despesas_total
    despesa_edit = Despesas.query.filter_by(id=id).first()
    tipos_despesa  = Tipos_despesa.query.filter_by(ativo="S").all()
    return render_template('edita_Reembolso-Adiantamento.html', user_session = nome_usuario.nome, reg_insert = reg_insert, intervalos = intervalos, despesas = despesas,
     despesa_edit = despesa_edit, despesas_total = despesas_total, navpills = 'navpills_4', current_user=nome_usuario.login, permissions = permissions,
     tipos_despesa = tipos_despesa, aprovadores = aprovadores)


@app.route('/despesa/atualizar', methods=['POST',])
def atualizar_despesa():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    despesa = Despesas.query.filter_by(id=request.form['id']).first()
    despesa.dt_despesa = request.form['dt_despesa']
    despesa.tipo = request.form.get('tipo') if request.form.get('tipo') != None else despesa.tipo 
    despesa.quantidade = request.form['quantidade']
    despesa.valor_despesa = float(str(request.form['valor_despesa']).replace(',','.'))
    despesa.valor_total = float(despesa.quantidade) * despesa.valor_despesa
    despesa.observacao = request.form['observacao']
    db.session.add(despesa)
    db.session.commit()
    flash('Despesa editada com sucesso!')
    return redirect(url_for('edita_reemb_adian', reg_insert = despesa.id_lancamento, navpills = 'navpills_4'))

@app.route('/despesas/deletar/<int:id>/<int:id_lancamento>')
def deletar_despesa(id, id_lancamento):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    Despesas.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Despesa deletada com sucesso!')
    return redirect(url_for('edita_reemb_adian', reg_insert=id_lancamento, navpills = 'navpills_4'))

#######################################INICIO UPLOAD ARQUIVOS DE DESPESAS#######################################
@app.route('/upload_despesas/<int:id_lancamento>/<int:id>')
def upload_despesa(id_lancamento, id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    permissions = {}
    permissions = permissoes(permissions)
    aprovadores = {}
    aprovadores = aprovador(aprovadores)
    id_lancamento = id_lancamento
    reg_insert = Lancamentos.query.filter_by(id=id_lancamento).first()
    intervalos = Intervalos.query.filter_by(id_lancamento=id_lancamento).order_by(Intervalos.id)
    despesas = Despesas.query.filter_by(id_lancamento=id_lancamento).order_by(Despesas.id)
    nome_usuario = Usuarios.query.filter_by(login=session['usuario_logado']).first()
    despesas_total = 0
    for despesa in despesas:
        despesas_total = despesas_total + despesa.valor_total
    despesas_total = despesas_total
    despesa_edit_upload = Despesas.query.filter_by(id=id).first()
    return render_template('edita_Reembolso-Adiantamento.html', user_session = nome_usuario.nome, reg_insert = reg_insert, intervalos = intervalos, despesas = despesas,
     despesa_edit_upload = despesa_edit_upload, despesas_total = despesas_total, navpills = 'navpills_4', current_user=nome_usuario.login, permissions = permissions,
     aprovadores = aprovadores)
# configurar o caminho de destino para os arquivos de upload
# obter o caminho da pasta atual
current_dir = os.path.abspath(os.path.dirname(__file__))

# definir o caminho de destino para os arquivos de upload
UPLOAD_FOLDER = os.path.join(current_dir, 'static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# definir a lista de extensões permitidas
ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_despesas/<int:id_lancamento>/<int:id>', methods=['POST',])
def upload_file(id_lancamento, id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    if request.method == 'POST':
        # verificar se o post request tem a parte do arquivo
        if 'file' not in request.files:
            flash('Nenhum arquivo selecionado')
            return redirect(request.url)
        file = request.files['file']
        # se o usuário não selecionar o arquivo, o navegador também
        # envia uma parte vazia sem o nome do arquivo
        if file.filename == '':
            flash('Nenhum arquivo selecionado')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # Separa o nome do arquivo da extensão
            name, ext = os.path.splitext(file.filename)
            #Query para pegar o tipo da despesa e passar no arquivo
            query = text(f'''select t1.*, t2.descricao from 
                        app_admin.despesas t1
                        inner join app_admin.tipos_despesa t2 on t2.id = t1.tipo
                        where t1.id = {id}''')
            despesa = Despesas_Query.query.from_statement(query).first()
            # Aplica o novo nome ao arquivo
            file.filename = f"RDV_{id_lancamento}_{despesa.descricao}_{id}{ext}"
            # Salva o arquivo no servidor usando o secure_filename para evitar problemas de segurança
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #faz update na tabela despesas setando o campo anexo = S para informar que tem comprovante de despesa
            despesa = Despesas.query.filter_by(id=id).first()
            despesa.anexo = 'S'
            despesa.nome_arquivo = filename
            db.session.add(despesa)
            db.session.commit()
            flash('Comprovante de despesa inserido com sucesso!')
            # retorna a pagina de edição de lançamento com o modal de despesa ativo
            return redirect(url_for('edita_reemb_adian', reg_insert=id_lancamento, navpills = 'navpills_4'))
    return ...
    
#######################################FIM UPLOAD ARQUIVOS DE DESPESAS#######################################


#######################################EXIBIR COMPROVANTE DE DESPESAS#######################################

@app.route('/exibir_comprovante/<int:id_lancamento>/<string:nome_arquivo>')
def exibir_comprovante(id_lancamento,nome_arquivo):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    permissions = {}
    permissions = permissoes(permissions)

    aprovadores = {}
    aprovadores = aprovador(aprovadores)
    id_lancamento = id_lancamento
    reg_insert = Lancamentos.query.filter_by(id=id_lancamento).first()
    intervalos = Intervalos.query.filter_by(id_lancamento=id_lancamento).order_by(Intervalos.id)
    despesas = Despesas.query.filter_by(id_lancamento=id_lancamento).order_by(Despesas.id)
    nome_usuario = Usuarios.query.filter_by(login=session['usuario_logado']).first()
    despesas_total = 0
    for despesa in despesas:
        despesas_total = despesas_total + despesa.valor_total
    despesas_total = despesas_total
    despesa_exibir_comprovante = nome_arquivo
    return render_template('edita_Reembolso-Adiantamento.html', user_session = nome_usuario.nome, reg_insert = reg_insert, 
     intervalos = intervalos, despesas = despesas,
     despesa_exibir_comprovante = despesa_exibir_comprovante, despesas_total = despesas_total, navpills = 'navpills_4', current_user=nome_usuario.login, permissions = permissions,
     aprovadores = aprovadores)

#######################################FIM EXIBIR COMPROVANTE DE DESPESAS#######################################
