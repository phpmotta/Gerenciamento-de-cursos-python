# Código para criação da janela virtual(interface)

import tkinter as tk
from tkinter import messagebox
import Admin  

def botao_salvar_click():
    
    nome = entrada_nome.get()
    descricao = entrada_desc.get()

    if not nome or not descricao:
        messagebox.showwarning("Atenção", "Preencha todos os campos!")
        return

    # passa os dados fornecidos para o arquivo Admin
    resultado = Admin.cadastrar_curso(nome, descricao)

    if resultado == "Sucesso":
        messagebox.showinfo("Parabéns", "Curso cadastrado com sucesso!")

        entrada_nome.delete(0, tk.END)
        entrada_desc.delete(0, tk.END)
    else:
        messagebox.showerror("Erro", resultado)

# Dimensão e título da janela
janela = tk.Tk()
janela.title("Sistema CEFET/RJ - Cadastro de Cursos")
janela.geometry("400x300")


label_titulo = tk.Label(janela, text="Cadastrar Novo Curso", font=("Arial", 16, "bold"))
label_titulo.pack(pady=20) 

label_nome = tk.Label(janela, text="Nome do Curso:")
label_nome.pack()
entrada_nome = tk.Entry(janela, width=40)
entrada_nome.pack(pady=5)

label_desc = tk.Label(janela, text="Descrição:")
label_desc.pack()
entrada_desc = tk.Entry(janela, width=40)
entrada_desc.pack(pady=5)

btn_salvar = tk.Button(janela, text="Salvar no Banco", command=botao_salvar_click, bg="green", fg="white")
btn_salvar.pack(pady=20)

janela.mainloop()