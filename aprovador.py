import mysql.connector
from mysql.connector import errorcode


def aprovador(aprovadores):
    print("Conectando...")
    try:
        conn = mysql.connector.connect(
                host='127.0.0.1',
                user='root',
                password='123456'
        )
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print('Existe algo errado no nome de usuário ou senha')
        else:
                print(err)

    cursor = conn.cursor()

    cursor.execute('''select t1.login, t2.aprovador from app_admin.usuarios t1
                    inner join app_admin.perfil_usuario t2 on t2.id = t1.id_perfil;''')
    aprovadores = {}
    for login, aprovador in cursor.fetchall():
        if login not in aprovadores:
            aprovadores[login] = []
        aprovadores[login].append(aprovador)
        
    return aprovadores

aprovadores = {}
aprovadores = aprovador(aprovadores)
#print(aprovadores)

