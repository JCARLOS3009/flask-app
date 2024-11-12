import sqlite3  # Adicione a importação do sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


# Função para conectar ao banco de dados SQLite
def conectar():
    conn = sqlite3.connect('pessoas.db')  # Conectando ao banco de dados SQLite
    return conn

# Criar a tabela 'pessoa' no banco de dados
def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS pessoa (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        idade INTEGER NOT NULL,
                        email TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Criar uma nova pessoa (agora com a rota '/pessoa')
@app.route('/pessoa', methods=['POST'])
def criar_pessoa():
    nome = request.form['nome']
    idade = request.form['idade']
    email = request.form['email']

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO pessoa (nome, idade, email) VALUES (?, ?, ?)', (nome, idade, email))
    conn.commit()
    conn.close()

    # Redireciona de volta para a página inicial (index)
    return "Cadastro realizado com sucesso!"


# Página inicial que redireciona para /pessoas
@app.route('/')
def home():
    return redirect(url_for('pessoas'))  # Redireciona para a rota que lista as pessoas

# Página que lista as pessoas
@app.route('/pessoas')
def pessoas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pessoa')
    pessoas = cursor.fetchall()
    conn.close()

    # Renderiza a página de listagem com as pessoas
    return render_template('index.html', pessoas=pessoas)


# Excluir uma pessoa
@app.route('/excluir/<int:id>', methods=['GET'])
def excluir(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM pessoa WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    # Redireciona para a página que lista as pessoas
    return redirect(url_for('pessoas'))  # Altere de 'index' para 'pessoas'


# Editar uma pessoa
@app.route('/pessoa/<int:id>', methods=['GET', 'POST'])
def editar(id):
    conn = conectar()
    cursor = conn.cursor()
    if request.method == 'POST':
        nome = request.form['nome']
        idade = request.form['idade']
        email = request.form['email']
        cursor.execute('''UPDATE pessoa SET nome = ?, idade = ?, email = ? WHERE id = ?''', 
                       (nome, idade, email, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    cursor.execute('SELECT * FROM pessoa WHERE id = ?', (id,))
    pessoa = cursor.fetchone()
    conn.close()
    return render_template('editar.html', pessoa=pessoa)

if __name__ == '__main__':
    criar_tabela()  # Cria a tabela 'pessoa' se ela não existir
    app.run(debug=True)
