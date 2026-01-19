# interface gráfica do programa

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import Admin
import ConectaMySQL
import Relatorios

# função para abrir janela do cadastro de curso
def abrir_janela_cadastro_curso():

    # janela de formulario
    janela_curso = tk.Toplevel()
    janela_curso.title("Admin - Cadastrar Curso")
    janela_curso.geometry("400x300")

    # título
    tk.Label(janela_curso, text="Novo Curso", font=("Arial", 14, "bold")).pack(pady=10)

    # campos
    tk.Label(janela_curso, text="Nome do Curso:").pack()
    entrada_nome = tk.Entry(janela_curso, width=40)
    entrada_nome.pack(pady=5)

    tk.Label(janela_curso, text="Descrição:").pack()
    entrada_desc = tk.Entry(janela_curso, width=40)
    entrada_desc.pack(pady=5)

    # função interna do botão salvar
    def salvar():
        nome = entrada_nome.get()
        descricao = entrada_desc.get()
        
        msg = Admin.cadastrar_curso(nome, descricao)
        
        if msg == "Sucesso":
            messagebox.showinfo("Sucesso", "Curso salvo no banco!")
            janela_curso.destroy()
        else:
            messagebox.showerror("Erro", msg)

    tk.Button(janela_curso, text="Salvar", bg="green", fg="white", command=salvar).pack(pady=20)

# função para o login genérico
def abrir_login_generico(tipo_perfil):

    # cria janela de login
    janela_login = tk.Toplevel()
    janela_login.title(f"Acesso Restrito - {tipo_perfil.capitalize()}")
    janela_login.geometry("300x200")

    # campo ID
    tk.Label(janela_login, text=f"ID de {tipo_perfil.capitalize()}:").pack(pady=5)
    ent_id = tk.Entry(janela_login)
    ent_id.pack(pady=5)

    # campo Senha 
    tk.Label(janela_login, text="Senha:").pack(pady=5)
    ent_senha = tk.Entry(janela_login, show="*") 
    ent_senha.pack(pady=5)

    def verificar_login():
        id_digitado = ent_id.get()
        senha_digitada = ent_senha.get()

        if not id_digitado or not senha_digitada:
            messagebox.showwarning("Atenção", "Digite ID e Senha!")
            return

        conn = ConectaMySQL.conectar()
        cursor = conn.cursor()
        
        # verifica id, senha e tipo de perfil
        sql = "SELECT nome FROM usuarios WHERE id = %s AND senha = %s AND tipo_perfil = %s"
        cursor.execute(sql, (id_digitado, senha_digitada, tipo_perfil))
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            nome_usuario = resultado[0]
            messagebox.showinfo("Bem-vindo!", f"Olá, {nome_usuario}!\nLogin realizado.")
            janela_login.destroy()
            
            if tipo_perfil == "aluno":
                abrir_janela_aluno(id_digitado, nome_usuario)
            elif tipo_perfil == "professor":
                abrir_janela_professor(id_digitado, nome_usuario)
        else:
            messagebox.showerror("Erro", "ID ou Senha incorretos!")

    tk.Button(janela_login, text="Entrar", bg="#3498db", fg="white", command=verificar_login).pack(pady=20)

# função para abrir menu do ADMIN
def abrir_menu_admin():

    # janela com botoes para admin
    janela_admin = tk.Toplevel()
    janela_admin.title("Área do Administrador")
    janela_admin.geometry("300x200")

    tk.Label(janela_admin, text="O que deseja fazer?", font=("Arial", 12)).pack(pady=20)

    # botão que leva para o formulário de curso
    btn_curso = tk.Button(janela_admin, text="Cadastrar Novo Curso", width=25, command=abrir_janela_cadastro_curso)
    btn_curso.pack(pady=10)

    btn_user = tk.Button(janela_admin, text="Cadastrar Usuário", width=25, command=abrir_janela_cadastro_usuario)
    btn_user.pack(pady=10)

# função para abrir janela de cadastro de usuario
def abrir_janela_cadastro_usuario():
    janela_user = tk.Toplevel()
    janela_user.title("Admin - Cadastrar Usuário")
    janela_user.geometry("400x450")

    tk.Label(janela_user, text="Novo Usuário", font=("Arial", 14, "bold")).pack(pady=10)

    # campo Nome
    tk.Label(janela_user, text="Nome Completo:").pack()
    ent_nome = tk.Entry(janela_user, width=40)
    ent_nome.pack(pady=5)

    # campo email
    tk.Label(janela_user, text="E-mail:").pack()
    ent_email = tk.Entry(janela_user, width=40)
    ent_email.pack(pady=5)

    # campo senha 
    tk.Label(janela_user, text="Senha:").pack()
    ent_senha = tk.Entry(janela_user, width=40, show="*")
    ent_senha.pack(pady=5)

    # seleção de perfil
    tk.Label(janela_user, text="Tipo de Perfil:").pack()
    combo_perfil = ttk.Combobox(janela_user, values=["admin", "professor", "aluno"], state="readonly")
    combo_perfil.current(2) 
    combo_perfil.pack(pady=5)

    # botão salvar
    def salvar_user():
        n = ent_nome.get()
        e = ent_email.get()
        s = ent_senha.get()
        p = combo_perfil.get() 

        if not n or not e or not s:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return

        msg = Admin.cadastrar_usuario(n, e, s, p)

        if msg == "Sucesso":
            messagebox.showinfo("Sucesso", f"Usuário {n} cadastrado!")
            janela_user.destroy()
        else:
            messagebox.showerror("Erro", msg)

    tk.Button(janela_user, text="Salvar Usuário", bg="#3498db", fg="white", command=salvar_user).pack(pady=20)

# função para abrir janela do menu de ALUNO
def abrir_janela_aluno(id_aluno, nome):
    janela = tk.Toplevel()
    janela.title(f"Portal do Aluno - {nome}")
    janela.geometry("400x300")

    tk.Label(janela, text=f"Bem-vindo, {nome}", font=("Arial", 14, "bold")).pack(pady=20)
    tk.Label(janela, text=f"ID: {id_aluno}", fg="gray").pack()

    # botao de matricula
    btn_mat = tk.Button(janela, text="Realizar Matrícula", width=30, height=2, bg="#2ecc71", fg="white",
                        command=lambda: messagebox.showinfo("A matrícula pode ser feita via terminal."))
    btn_mat.pack(pady=10)
    
    # botão sair
    tk.Button(janela, text="Sair", command=janela.destroy).pack(pady=20)

#função para abrir janela menu do PROFESSOR
def abrir_janela_professor(id_prof, nome):
    janela = tk.Toplevel()
    janela.title(f"Portal do Professor - {nome}")
    janela.geometry("400x300")

    tk.Label(janela, text=f"Prof. {nome}", font=("Arial", 14, "bold")).pack(pady=20)
    
    # botao lançar notas (incompleto)
    btn_notas = tk.Button(janela, text="Lançar Notas", width=30, height=2, bg="#e67e22", fg="white",
                          command=lambda: messagebox.showinfo("O lançamento de notas pode ser feito via Terminal."))
    btn_notas.pack(pady=10)

    # botão sair
    tk.Button(janela, text="Sair", command=janela.destroy).pack(pady=20)

# função para abrir janela dos relatorios
def abrir_janela_relatorios():
    janela_rel = tk.Toplevel()
    janela_rel.title("Relatórios e Estatísticas")
    janela_rel.geometry("300x250")

    tk.Label(janela_rel, text="Selecione o Relatório", font=("Arial", 12, "bold")).pack(pady=15)

    # mostra o resultado em uma caixa de mensagem
    def mostrar_top3():
        texto = Relatorios.get_relatorio_top3()
        messagebox.showinfo("Top 3 Turmas", texto)

    def mostrar_reprovados():
        texto = Relatorios.get_relatorio_reprovados()
        messagebox.showinfo("Alunos Reprovados", texto)

    def rodar_arquivamento():
        texto = Relatorios.executar_arquivamento_gui()
        messagebox.showinfo("Manutenção", texto)

    # botões
    tk.Button(janela_rel, text="Top 3 Melhores Turmas", width=25, command=mostrar_top3).pack(pady=5)
    tk.Button(janela_rel, text="Alunos em Recuperação", width=25, command=mostrar_reprovados).pack(pady=5)
    tk.Button(janela_rel, text="Arquivar Turmas Vencidas", width=25, command=rodar_arquivamento, bg="#f39c12", fg="white").pack(pady=15)

# tela principal
janela_principal = tk.Tk()
janela_principal.title("Sistema de Gestão CEFET/RJ")
janela_principal.geometry("500x400")

# titulo
tk.Label(janela_principal, text="Bem-vindo ao Sistema Acadêmico", font=("Arial", 18, "bold")).pack(pady=40)
tk.Label(janela_principal, text="Selecione seu perfil:", font=("Arial", 12)).pack(pady=10)

# botões menu
frame_botoes = tk.Frame(janela_principal)
frame_botoes.pack()

# botão ADMIN
btn_admin = tk.Button(frame_botoes, text="ADMINISTRADOR", bg="#3498db", fg="white", font=("Arial", 10, "bold"), 
                      width=20, height=2, command=abrir_menu_admin)
btn_admin.pack(pady=10)

# botão PROFESSOR 
btn_prof = tk.Button(frame_botoes, text="PROFESSOR", bg="#e67e22", fg="white", font=("Arial", 10, "bold"), 
                     width=20, height=2, command=lambda: abrir_login_generico("professor"))
btn_prof.pack(pady=10)

# botão ALUNO 
btn_aluno = tk.Button(frame_botoes, text="ALUNO", bg="#2ecc71", fg="white", font=("Arial", 10, "bold"), 
                      width=20, height=2, command=lambda: abrir_login_generico("aluno"))
btn_aluno.pack(pady=10)

#botão relatórios
btn_rel = tk.Button(frame_botoes, text="RELATÓRIOS (Geral)", bg="#8e44ad", fg="white", font=("Arial", 10, "bold"), 
                    width=20, height=2, command=abrir_janela_relatorios)
btn_rel.pack(pady=10)

# detalhe rodapé
tk.Label(janela_principal, text="Trabalho de Banco de Dados - 2025", fg="gray").pack(side="bottom", pady=10)

janela_principal.mainloop()