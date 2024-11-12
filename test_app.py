import unittest
from app import app, conectar  # Importa a aplicação Flask e a função de conexão ao banco de dados

class TestApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Configuração do banco de dados e da aplicação para os testes"""
        cls.app = app.test_client()  # Cliente de teste do Flask
        cls.app.testing = True
        cls.conn = conectar()
        cls.cursor = cls.conn.cursor()
        # Criação da tabela 'pessoa' no banco de dados, caso não exista
        cls.cursor.execute('''CREATE TABLE IF NOT EXISTS pessoa (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                nome TEXT NOT NULL,
                                idade INTEGER NOT NULL,
                                email TEXT NOT NULL)''')
        cls.conn.commit()

    @classmethod
    def tearDownClass(cls):
        """Limpeza após todos os testes"""
        # Exclui a tabela 'pessoa' após os testes para garantir que o banco esteja limpo
        cls.cursor.execute('DROP TABLE IF EXISTS pessoa')
        cls.conn.commit()
        cls.conn.close()

    def setUp(self):
        """Limpeza da tabela antes de cada teste"""
        # Exclui todos os registros da tabela 'pessoa' antes de cada teste
        self.cursor.execute('DELETE FROM pessoa')
        self.conn.commit()

    def test_criar_pessoa(self):
        """Teste de criação de uma pessoa"""
        response = self.app.post('/pessoa', data=dict(nome='João', idade=30, email='joao@example.com'))
        
        # Espera a resposta com a mensagem de sucesso
        self.assertEqual(response.data.decode('utf-8'), 'Cadastro realizado com sucesso!')  # Verifica o texto de sucesso

        # Verifica se a pessoa foi criada no banco de dados
        self.cursor.execute('SELECT * FROM pessoa WHERE nome = ?', ('João',))
        pessoa = self.cursor.fetchone()
        self.assertIsNotNone(pessoa)  # A pessoa deve existir no banco
        self.assertEqual(pessoa[1], 'João')  # Verifica o nome
        self.assertEqual(pessoa[2], 30)  # Verifica a idade
        self.assertEqual(pessoa[3], 'joao@example.com')  # Verifica o email

    def test_listar_pessoas(self):
        """Teste para listar as pessoas"""
        # Cria uma nova pessoa
        self.app.post('/pessoa', data=dict(nome='João', idade=30, email='joao@example.com'))

        # Faz uma requisição GET para listar as pessoas
        response = self.app.get('/pessoas')

        # Verifica se a resposta tem o nome da pessoa criada
        self.assertEqual(response.status_code, 200)  # Espera um código de status 200 (OK)
        self.assertIn('João', response.data.decode('utf-8'))  # Verifica se 'João' está na resposta, decodificando para string

    def test_excluir_pessoa(self):
        """Teste para excluir uma pessoa"""
        # Cria uma nova pessoa
        self.app.post('/pessoa', data=dict(nome='João', idade=30, email='joao@example.com'))

        # Verifica se a pessoa foi criada
        self.cursor.execute('SELECT * FROM pessoa WHERE nome = ?', ('João',))
        pessoa = self.cursor.fetchone()
        pessoa_id = pessoa[0]  # Obtém o ID da pessoa criada

        # Faz uma requisição para excluir a pessoa
        response = self.app.get(f'/excluir/{pessoa_id}')

        # Verifica se a pessoa foi excluída
        self.cursor.execute('SELECT * FROM pessoa WHERE id = ?', (pessoa_id,))
        pessoa_excluida = self.cursor.fetchone()
        self.assertIsNone(pessoa_excluida)  # A pessoa deve ser removida do banco de dados

        # Verifica se o redirecionamento ocorreu corretamente (status 302)
        self.assertEqual(response.status_code, 302)

if __name__ == '__main__':
    unittest.main()
import unittest
from app import app, conectar  # Importa a aplicação Flask e a função de conexão ao banco de dados

class TestApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Configuração do banco de dados e da aplicação para os testes"""
        cls.app = app.test_client()  # Cliente de teste do Flask
        cls.app.testing = True
        cls.conn = conectar()
        cls.cursor = cls.conn.cursor()
        # Criação da tabela 'pessoa' no banco de dados, caso não exista
        cls.cursor.execute('''CREATE TABLE IF NOT EXISTS pessoa (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                nome TEXT NOT NULL,
                                idade INTEGER NOT NULL,
                                email TEXT NOT NULL)''')
        cls.conn.commit()

    @classmethod
    def tearDownClass(cls):
        """Limpeza após todos os testes"""
        # Exclui a tabela 'pessoa' após os testes para garantir que o banco esteja limpo
        cls.cursor.execute('DROP TABLE IF EXISTS pessoa')
        cls.conn.commit()
        cls.conn.close()

    def setUp(self):
        """Limpeza da tabela antes de cada teste"""
        # Exclui todos os registros da tabela 'pessoa' antes de cada teste
        self.cursor.execute('DELETE FROM pessoa')
        self.conn.commit()

    def test_criar_pessoa(self):
        """Teste de criação de uma pessoa"""
        response = self.app.post('/pessoa', data=dict(nome='João', idade=30, email='joao@example.com'))
        
        # Espera a resposta com a mensagem de sucesso
        self.assertEqual(response.data.decode('utf-8'), 'Cadastro realizado com sucesso!')  # Verifica o texto de sucesso

        # Verifica se a pessoa foi criada no banco de dados
        self.cursor.execute('SELECT * FROM pessoa WHERE nome = ?', ('João',))
        pessoa = self.cursor.fetchone()
        self.assertIsNotNone(pessoa)  # A pessoa deve existir no banco
        self.assertEqual(pessoa[1], 'João')  # Verifica o nome
        self.assertEqual(pessoa[2], 30)  # Verifica a idade
        self.assertEqual(pessoa[3], 'joao@example.com')  # Verifica o email

    def test_listar_pessoas(self):
        """Teste para listar as pessoas"""
        # Cria uma nova pessoa
        self.app.post('/pessoa', data=dict(nome='João', idade=30, email='joao@example.com'))

        # Faz uma requisição GET para listar as pessoas
        response = self.app.get('/pessoas')

        # Verifica se a resposta tem o nome da pessoa criada
        self.assertEqual(response.status_code, 200)  # Espera um código de status 200 (OK)
        self.assertIn('João', response.data.decode('utf-8'))  # Verifica se 'João' está na resposta, decodificando para string

    def test_excluir_pessoa(self):
        """Teste para excluir uma pessoa"""
        # Cria uma nova pessoa
        self.app.post('/pessoa', data=dict(nome='João', idade=30, email='joao@example.com'))

        # Verifica se a pessoa foi criada
        self.cursor.execute('SELECT * FROM pessoa WHERE nome = ?', ('João',))
        pessoa = self.cursor.fetchone()
        pessoa_id = pessoa[0]  # Obtém o ID da pessoa criada

        # Faz uma requisição para excluir a pessoa
        response = self.app.get(f'/excluir/{pessoa_id}')

        # Verifica se a pessoa foi excluída
        self.cursor.execute('SELECT * FROM pessoa WHERE id = ?', (pessoa_id,))
        pessoa_excluida = self.cursor.fetchone()
        self.assertIsNone(pessoa_excluida)  # A pessoa deve ser removida do banco de dados

        # Verifica se o redirecionamento ocorreu corretamente (status 302)
        self.assertEqual(response.status_code, 302)

if __name__ == '__main__':
    unittest.main()
