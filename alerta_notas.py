import sqlite3
import smtplib
from email.message import EmailMessage
import os

def criar_banco_de_dados():
    conexao = sqlite3.connect('Escola.db')
    cursor = conexao.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS alunos_notas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email_responsavel TEXT NOT NULL,
        nota REAL NOT NULL
    )
    ''')
    conexao.commit()
    conexao.close()

def inserir_dados_exemplo():
    conexao = sqlite3.connect('Escola.db')
    cursor = conexao.cursor()
    cursor.execute("SELECT COUNT(*) FROM alunos_notas")
    if cursor.fetchone()[0] == 0:
        dados_alunos = [
            ('João Silva', 'joao.responsavel@email.com', 8.5),
            ('Maria Souza', 'pedrovictoru@gmail.com', 6.8),
            ('Pedro Santos', 'pedro.responsavel@email.com', 9.1),
            ('Ana Oliveira', 'pedrovictoru@gmail.com', 5.5),
            ('Carlos Lima', 'carlos.responsavel@email.com', 7.0)
        ]
        cursor.executemany("INSERT INTO alunos_notas (nome, email_responsavel, nota) VALUES (?, ?, ?)", dados_alunos)
        conexao.commit()
    conexao.close()

def buscar_alunos_em_risco():
    conexao = sqlite3.connect('Escola.db')
    cursor = conexao.cursor()
    query = "SELECT nome, email_responsavel, nota FROM alunos_notas WHERE nota < 7.0"
    cursor.execute(query)
    alunos_em_risco = cursor.fetchall()
    conexao.close()
    return alunos_em_risco

def enviar_email_alerta(lista_alunos):
    msg = EmailMessage()
    msg['Subject'] = '⚠️ RELATÓRIO: Alunos com Baixo Desempenho'
    msg['From'] = 'pedrovictoru@gmail.com'
    msg['To'] = 'pedrovictoru@gmail.com' # Enviando para você mesmo como teste

    corpo = "Prezada Coordenação,\n\nOs seguintes alunos foram identificados com nota abaixo de 7.0:\n\n"
    for aluno in lista_alunos:
        corpo += f"- Aluno: {aluno[0]} | Nota: {aluno[2]} | Responsável: {aluno[1]}\n"
    
    corpo += "\nEste é um e-mail automático gerado pelo sistema de monitoramento."
    msg.set_content(corpo)

    # O GitHub Actions vai buscar aquela senha de 16 letras que você salvou no Secret
    senha = os.environ.get('EMAIL_PASSWORD') 

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(msg['From'], senha)
        smtp.send_message(msg)

if __name__ == "__main__":
    criar_banco_de_dados()
    inserir_dados_exemplo()
    lista = buscar_alunos_em_risco()
    
    if lista:
        print(f"Encontrados {len(lista)} alunos em risco. Enviando e-mail...")
        enviar_email_alerta(lista)
        print("E-mail enviado com sucesso!")
    else:
        print("Nenhum aluno em risco identificado.")
