SECRET_KEY = 'master'

SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = '123456',
        servidor = '127.0.0.1',
        database = 'app_admin'
    )

#master e master123