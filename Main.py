# menu inicial do programa
import Admin
import Aluno
import Professor
import Relatorios

while True:
    print("\n=== SISTEMA DE GESTÃO CEFET/RJ ===")
    print("1. [Admin] Listar Cursos")
    print("2. [Admin] Cadastrar Novo Curso")
    print("3. [Admin] Cadastrar Usuário")
    print("4. [Admin] Criar Turma")     
    print("5. [Aluno] Fazer Matrícula") 
    print("6. [Professor] Área do Professor (Notas)")
    print("7. [Geral] Relatórios e Estatísticas")
    print("0. Sair")
    
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        Admin.listar_cursos()
    elif opcao == "2":
        Admin.cadastrar_curso()
    elif opcao == "3":
        Admin.cadastrar_usuario()
    elif opcao == "4":
        Admin.criar_turma()   
    elif opcao == "5":
        Aluno.realizar_matricula()  
    elif opcao == "6":
        Professor.area_professor()
    elif opcao == "7":
            Relatorios.menu_relatorios()
    elif opcao == "0":
        break