from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração da conexão com o banco de dados PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://default:Ew4LKOoIpBv5@ep-falling-hall-a43wfsot.us-east-1.aws.neon.tech:5432/verceldb?sslmode=require'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desabilita a rastreabilidade de modificações (opcional)

db = SQLAlchemy(app)

# Definindo um modelo de exemplo
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

@app.route('/')
def index():
    user = User.query.first()  # Exemplo de consulta ao banco
    return f"Hello, {user.username}!" if user else "No user found!"

if __name__ == '__main__':
    app.run(debug=True)
