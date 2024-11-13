from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração da conexão com o banco de dados PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://default:Ew4LKOoIpBv5@ep-falling-hall-a43wfsot.us-east-1.aws.neon.tech:5432/verceldb?sslmode=require'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desabilita rastreabilidade de modificações

db = SQLAlchemy(app)

# Definindo o modelo de dados (Tabela "pessoa")
class Pessoa(db.Model):
    __tablename__ = 'pessoa'  # Nome da tabela no banco

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<Pessoa {self.nome}>'

# Criar as tabelas no banco de dados (em vez de usar @app.before_first_request)
def create_tables():
    with app.app_context():
        db.create_all()  # Cria as tabelas no banco de dados

# Página inicial que redireciona para /pessoas
@app.route('/')
def home():
    return redirect(url_for('pessoas'))  # Redireciona para a rota que lista as pessoas

# Página que lista todas as pessoas
@app.route('/pessoas')
def pessoas():
    pessoas = Pessoa.query.all()  # Consulta todas as pessoas
    return render_template('index.html', pessoas=pessoas)  # Renderiza a página com a lista

# Criar uma nova pessoa
@app.route('/pessoa', methods=['POST'])
def criar_pessoa():
    nome = request.form['nome']
    idade = request.form['idade']
    email = request.form['email']

    # Cria um novo objeto Pessoa e adiciona ao banco
    nova_pessoa = Pessoa(nome=nome, idade=idade, email=email)
    db.session.add(nova_pessoa)
    db.session.commit()

    return redirect(url_for('pessoas'))  # Redireciona para a página que lista as pessoas

# Excluir uma pessoa
@app.route('/excluir/<int:id>', methods=['GET'])
def excluir(id):
    pessoa = Pessoa.query.get(id)
    if pessoa:
        db.session.delete(pessoa)
        db.session.commit()
    return redirect(url_for('pessoas'))  # Redireciona para a lista de pessoas

# Editar uma pessoa
@app.route('/pessoa/<int:id>', methods=['GET', 'POST'])
def editar(id):
    pessoa = Pessoa.query.get(id)

    if request.method == 'POST':
        pessoa.nome = request.form['nome']
        pessoa.idade = request.form['idade']
        pessoa.email = request.form['email']
        
        db.session.commit()
        return redirect(url_for('pessoas'))  # Redireciona para a lista de pessoas

    return render_template('editar.html', pessoa=pessoa)  # Página de edição

# Chamando a função de criar tabelas logo após a inicialização
create_tables()

if __name__ == '__main__':
    app.run(debug=True)
