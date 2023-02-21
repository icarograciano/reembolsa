from config_mysql import conn


def aprovador(aprovadores):

    cursor = conn.cursor()

    cursor.execute('''select t1.login, t2.aprovador from app_admin.usuarios t1
                    inner join app_admin.perfil_usuario t2 on t2.id = t1.id_perfil;''')
    aprovadores = {}
    for login, aprovador in cursor.fetchall():
        if login not in aprovadores:
            aprovadores[login] = []
        aprovadores[login].append(aprovador)
    
    cursor.close()
    
    return aprovadores

aprovadores = {}
aprovadores = aprovador(aprovadores)
#print(aprovadores)


