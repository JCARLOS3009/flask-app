from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Necessário para exibir mensagens de erro com `flash`

# Configuração da conexão com o banco de dados PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://default:Ew4LKOoIpBv5@ep-falling-hall-a43wfsot.us-east-1.aws.neon.tech:5432/verceldb?sslmode=require'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definindo o modelo de dados (Tabela "pessoa")
class Pessoa(db.Model):
    __tablename__ = 'pessoa'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<Pessoa {self.nome}>'

# Criar as tabelas no banco de dados (em vez de usar @app.before_first_request)
def create_tables():
    with app.app_context():
        db.create_all()

@app.route('/')
def home():
    return redirect(url_for('pessoas'))

@app.route('/pessoas')
def pessoas():
    pessoas = Pessoa.query.all()
    return render_template('index.html', pessoas=pessoas)

# Criar uma nova pessoa
@app.route('/pessoa', methods=['POST'])
def criar_pessoa():
    nome = request.form['nome']
    idade = request.form['idade']
    email = request.form['email']

    # Verificar se o e-mail já existe
    pessoa_existente = Pessoa.query.filter_by(email=email).first()
    if pessoa_existente:
        flash(f"O e-mail {email} já está registrado. Por favor, utilize outro e-mail.")
        return redirect(url_for('pessoas'))

    # Tentar adicionar a nova pessoa ao banco
    nova_pessoa = Pessoa(nome=nome, idade=idade, email=email)
    db.session.add(nova_pessoa)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash(f"O e-mail {email} já está registrado.")
        return redirect(url_for('pessoas'))

    return redirect(url_for('pessoas'))

@app.route('/excluir/<int:id>', methods=['GET'])
def excluir(id):
    pessoa = Pessoa.query.get(id)
    if pessoa:
        db.session.delete(pessoa)
        db.session.commit()
    return redirect(url_for('pessoas'))

@app.route('/pessoa/<int:id>', methods=['GET', 'POST'])
def editar(id):
    pessoa = Pessoa.query.get(id)

    if request.method == 'POST':
        pessoa.nome = request.form['nome']
        pessoa.idade = request.form['idade']
        pessoa.email = request.form['email']

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("Erro ao atualizar: e-mail já está em uso.")
            return redirect(url_for('editar', id=id))

        return redirect(url_for('pessoas'))

    return render_template('editar.html', pessoa=pessoa)

# Chamando a função de criar tabelas
create_tables()

if __name__ == '__main__':
    app.run(debug=True)
