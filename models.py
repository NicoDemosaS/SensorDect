import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'sensordect.db')

def get_db_connection():
    """Cria uma conexão com o banco de dados"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_db():
    """Inicializa o banco de dados com a tabela de usuários"""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    print("Banco de dados inicializado.")

def create_user(username, password):
    """Cria um novo usuário no banco de dados"""
    conn = get_db_connection()
    hashed_password = generate_password_hash(password)
    conn.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                 (username, hashed_password))
    conn.commit()
    print("Usuário criado com sucesso: ", username)
    conn.close()

def verify_user(username, password):
    """Verifica as credenciais do usuário"""
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    if user and check_password_hash(user['password'], password):
        return True
    return False

