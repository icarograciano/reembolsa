from flask import render_template, request, redirect, session, flash, url_for
from app import app, db
from models import Despesas, Intervalos, Lancamentos, present_time 
import os
from werkzeug.utils import secure_filename

@app.route('/despesas/criar', methods=['POST',])
def criar_despesas():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    tipo = request.form['tipo']
    quantidade = float(request.form['quantidade'])
    valor_despesa = float(str(request.form['valor_despesa']).replace(',','.'))
    valor_total = quantidade * valor_despesa
    id_lancamento = request.form['id_lancamento']
    observacao = request.form['observacao']
    anexo = 'N'
    nova_despesa = Despesas(tipo = tipo, quantidade = quantidade, valor_despesa = valor_despesa, id_lancamento = id_lancamento, valor_total = valor_total,
    usuario_add = session['usuario_logado'] , usuario_edicao = session['usuario_logado'], data_add = f'''{present_time}''' , data_edicao = f'''{present_time}''',
    observacao = observacao, anexo = anexo)
    db.session.add(nova_despesa)
    db.session.commit()
    flash('Despesa criada com sucesso!')
    return redirect(url_for('edita_atendimento', reg_insert=id_lancamento, navpills = 'navpills_4'))

@app.route('/despesas/editar/<int:id_lancamento>/<int:id>')
def editar_despesa(id_lancamento, id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    id_lancamento = id_lancamento
    reg_insert = Lancamentos.query.filter_by(id=id_lancamento).first()
    intervalos = Intervalos.query.filter_by(id_lancamento=id_lancamento).order_by(Intervalos.id)
    despesas = Despesas.query.filter_by(id_lancamento=id_lancamento).order_by(Despesas.id)
    despesas_total = 0
    for despesa in despesas:
        despesas_total = despesas_total + despesa.valor_total
    despesas_total = despesas_total
    despesa_edit = Despesas.query.filter_by(id=id).first()
    return render_template('edita_atendimentos.html', user_session=session['usuario_logado'], reg_insert = reg_insert, intervalos = intervalos, despesas = despesas,
     despesa_edit = despesa_edit, despesas_total = despesas_total, navpills = 'navpills_4')


@app.route('/despesa/atualizar', methods=['POST',])
def atualizar_despesa():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    despesa = Despesas.query.filter_by(id=request.form['id']).first()
    despesa.tipo = request.form.get('tipo') if request.form.get('tipo') != None else despesa.tipo 
    despesa.quantidade = request.form['quantidade']
    despesa.valor_despesa = float(str(request.form['valor_despesa']).replace(',','.'))
    despesa.valor_total = float(despesa.quantidade) * despesa.valor_despesa
    despesa.observacao = request.form['observacao']
    db.session.add(despesa)
    db.session.commit()
    flash('Despesa editada com sucesso!')
    return redirect(url_for('edita_atendimento', reg_insert = despesa.id_lancamento, navpills = 'navpills_4'))

@app.route('/despesas/deletar/<int:id>/<int:id_lancamento>')
def deletar_despesa(id, id_lancamento):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    Despesas.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Despesa deletada com sucesso!')
    return redirect(url_for('edita_atendimento', reg_insert=id_lancamento, navpills = 'navpills_4'))

#######################################INICIO UPLOAD ARQUIVOS DE DESPESAS#######################################
@app.route('/upload_despesas/<int:id_lancamento>/<int:id>')
def upload_despesa(id_lancamento, id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    id_lancamento = id_lancamento
    reg_insert = Lancamentos.query.filter_by(id=id_lancamento).first()
    intervalos = Intervalos.query.filter_by(id_lancamento=id_lancamento).order_by(Intervalos.id)
    despesas = Despesas.query.filter_by(id_lancamento=id_lancamento).order_by(Despesas.id)
    despesas_total = 0
    for despesa in despesas:
        despesas_total = despesas_total + despesa.valor_total
    despesas_total = despesas_total
    despesa_edit_upload = Despesas.query.filter_by(id=id).first()
    return render_template('edita_atendimentos.html', user_session=session['usuario_logado'], reg_insert = reg_insert, intervalos = intervalos, despesas = despesas,
     despesa_edit_upload = despesa_edit_upload, despesas_total = despesas_total, navpills = 'navpills_4')
# configurar o caminho de destino para os arquivos de upload
# obter o caminho da pasta atual
current_dir = os.path.abspath(os.path.dirname(__file__))

# definir o caminho de destino para os arquivos de upload
UPLOAD_FOLDER = os.path.join(current_dir, 'arquivos')
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
            despesa = Despesas.query.filter_by(id=id).first()
            # Aplica o novo nome ao arquivo
            file.filename = f"RDV_{id_lancamento}_{despesa.tipo}_{id}{ext}"
            # Salva o arquivo no servidor usando o secure_filename para evitar problemas de segurança
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #faz update na tabela despesas setando o campo anexo = S para informar que tem comprovante de despesa
            despesa = Despesas.query.filter_by(id=id).first()
            despesa.anexo = 'S'
            db.session.add(despesa)
            db.session.commit()
            flash('Comprovante de despesa inserido com sucesso!')
            # retorna a pagina de edição de lançamento com o modal de despesa ativo
            return redirect(url_for('edita_atendimento', reg_insert=id_lancamento, navpills = 'navpills_4'))
    return ...
    
#######################################FIM UPLOAD ARQUIVOS DE DESPESAS#######################################

