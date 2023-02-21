# Sistema para Reembolso de Despesas Corporativas

# Introdução
Com poucos toques no Reembolsa, o relatório de despesas é criado e o colaborador nunca mais perderá cupons fiscais ou terá que ficar montando planilhas de despesas.

![image](https://user-images.githubusercontent.com/70548062/220225807-05abb1c1-f9d9-4276-a7e7-cf0c56892d54.png)


# Tecnologias utilizadas

Front-End: Bootstrap 4 (HTML, CSS e JS)
Back-end: Python(Flask) e Java Script (todas as bibliotecas python estão no arquivo requirements.txt)
BD: MySql 8.0
Framewrok para desenvolvimento de relatório: JasperSoftStudio e JasperServer


# Principais Funcionalidades

Rota de Cadastro de Usuário e Perfil de usuário
Rota de Alteração de Senha
Rota de Usuário e Autenticação
Rota de Controle de Permissão por tela e por pefil do tipo Aprovador
Rota de Cadastros de Configuração de Servidor para envio Email
Rota de Cadastros de Clientes
Rota de Cadastros de Motivos de Despesa
Rota de Cadastros de Tipos de Despesa
Rota de Lançamentos
Rota de Lançamentos de Despesas
Rota de Anexo de Comprovantes
Rota de Visualização dos Anexos
Rota de Impressão de relatório
Rota de Envio para Aprovação, Aprovação e Finalização de um processo
Rota de Envio de email automático a cada mudança de status do processo

# Como Instalar

1 - Tenha o banco mysql instalado e ajuste a suas credencias do banco no arquivo config.py e config_mysql.py

![image](https://user-images.githubusercontent.com/70548062/220225623-07e0ad43-ea21-4aa2-8c09-906580057e8a.png)


![image](https://user-images.githubusercontent.com/70548062/220225541-20ed9d75-2ec3-4a5a-83e1-d34b441f7596.png)


![image](https://user-images.githubusercontent.com/70548062/220225009-7c8dce5e-be46-48da-b178-af02eb855d35.png)


2 - Execute o arquivo prepara_banco.py para rodar todas as tabelas do essencias do programa

![image](https://user-images.githubusercontent.com/70548062/220225934-8f4d9d97-a7de-4cad-bf8e-d57b9079e962.png)


3 - Execute o arquivo app.py  para iniciar o servidor web do Flask configurando-o para executar em modo de depuração (debug=True) para que quaisquer erros possam ser facilmente identificados e corrigidos durante o desenvolvimento.

![image](https://user-images.githubusercontent.com/70548062/220226904-cd71e807-81d4-4d90-a32b-a51f34650082.png)

4 - Acesse http://127.0.0.1:5000/login e entre com a credencias:

login: reembolsa@reembolsa.com.br
senha: master

![image](https://user-images.githubusercontent.com/70548062/220227511-d7dd1b03-d352-4ee2-8ceb-ee259c97afa4.png)


![image](https://user-images.githubusercontent.com/70548062/220227494-b165ba95-b103-428f-b622-90bc957d8691.png)

5 - Cadastre: Clientes, Motivos, Tipos de Despesa e Configure o Servidor de Email

![image](https://user-images.githubusercontent.com/70548062/220228245-489462c3-675a-4d08-a169-bf7b6ff89997.png)

![image](https://user-images.githubusercontent.com/70548062/220228263-a506e6a8-d09f-4dcd-a881-40a22d713448.png)

![image](https://user-images.githubusercontent.com/70548062/220228278-a102d28f-4bb9-47f6-8607-145994da4504.png)

![image](https://user-images.githubusercontent.com/70548062/220228312-d79f5f90-ee4a-4749-a86e-b02f5f4b0d20.png)

5 - Cadastre e Configure conforme necessidade: Perfil de Usuario e Usuarios

![image](https://user-images.githubusercontent.com/70548062/220228412-b25553e0-3e0c-483b-a83e-0846cd96fe9a.png)

![image](https://user-images.githubusercontent.com/70548062/220228432-9e87fe30-106f-47ef-bf85-02d734f8b6b1.png)

![image](https://user-images.githubusercontent.com/70548062/220228447-6e660140-8e6c-471b-bfc2-2bf27c7d1bdc.png)

5 - Teste o Lançamento de Despesa

![image](https://user-images.githubusercontent.com/70548062/220230060-e08508b3-f2c5-4aad-bed7-669bc9ec1890.png)

![image](https://user-images.githubusercontent.com/70548062/220230075-a7668498-f35e-4680-9066-c2a1532745b9.png)

![image](https://user-images.githubusercontent.com/70548062/220230094-19035ded-7905-4c17-979e-9f60fdf28fc9.png)

![image](https://user-images.githubusercontent.com/70548062/220230121-a6423502-72b0-491b-94bf-72dbca6afc9c.png)

![image](https://user-images.githubusercontent.com/70548062/220230151-03837a28-7e50-4f33-adcc-ba2309b09fd2.png)

![image](https://user-images.githubusercontent.com/70548062/220230183-02907291-8b7d-4c5b-8a2c-e1f05a049889.png)

![image](https://user-images.githubusercontent.com/70548062/220230228-e31710d7-7f7e-4dc4-8610-700199d04dc5.png)

![image](https://user-images.githubusercontent.com/70548062/220230240-95c21077-6b73-4e45-99b8-1c8faed47b81.png)

![image](https://user-images.githubusercontent.com/70548062/220230259-846382d4-4a8f-4b47-b64d-4cd26ee00331.png)

![image](https://user-images.githubusercontent.com/70548062/220230272-e681ae4a-7f2d-4bbd-9d70-6f786c22f7e4.png)


# Considerações finais

Esse projeto ja funciona e vem sendo melhorado constantemente, até que ele chegue no seu padrão definitivo. Quem precisar de ajudar com o jasperserver me chama no privado. No mais, muito obrigado. 🙋‍♂️!

# Autor

Feito por Icaro Graciano. Dúvidas, entre em contato!

Linkdin: https://www.linkedin.com/in/icarograciano/
GitHub: https://github.com/icarograciano



