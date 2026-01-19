#Conecta o python ao MySQL

import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost", user="root", password="1234", database="gestao_cursos")