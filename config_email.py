from app import app, Mail
from config_mysql import conn


def dados_env_email():

    cursor = conn.cursor()

    cursor.execute('''SELECT id, servidor, porta, ssl_email, usuario, senha FROM app_admin.config_email WHERE id=1''')
    resultado = cursor.fetchone()
    id = resultado[0]
    servidor = resultado[1]
    porta = resultado[2]
    ssl_email = resultado[3]
    usuario = resultado[4]
    senha = resultado[5]

    cursor.close()

    # Retorna os valores como uma tupla
    return (servidor, porta, ssl_email, usuario, senha)

# Chama a função dados_env_email e atribui os valores retornados às variáveis de configuração do Flask
servidor, porta, ssl_email, usuario, senha = dados_env_email()

app.config['MAIL_SERVER'] = servidor
app.config['MAIL_PORT'] = porta
app.config['MAIL_USE_SSL'] = ssl_email
app.config['MAIL_USERNAME'] = usuario
app.config['MAIL_PASSWORD'] = senha

mail = Mail(app)


