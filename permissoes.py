import mysql.connector
from mysql.connector import errorcode


def permissoes(permissions):
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

    cursor.execute('''select distinct
                    t1.login, t2.tela
                    from app_admin.usuarios t1
                    inner join app_admin.perfil_usuario_det t2 on t2.cod_perfil = t1.id_perfil
                    where t2.mostrar = 'S'
                    order by t1.login;''')
    permissions = {}
    for login, tela in cursor.fetchall():
        if login not in permissions:
            permissions[login] = []
        permissions[login].append(tela)
        
    return permissions

permissions = {}
permissions = permissoes(permissions)
#print(permissions)
