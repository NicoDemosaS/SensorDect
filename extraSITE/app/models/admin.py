import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db


class Admin(UserMixin, db.Model):
    """Modelo do Administrador."""
    
    __tablename__ = 'admins'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    nome = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    senha_hash = db.Column(db.String(256), nullable=False)
    
    # Status
    ativo = db.Column(db.Boolean, default=True)
    
    # Timestamps
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    ultimo_login = db.Column(db.DateTime, nullable=True)
    
    def set_senha(self, senha):
        """Define a senha do admin (hash)."""
        self.senha_hash = generate_password_hash(senha)
    
    def check_senha(self, senha):
        """Verifica se a senha está correta."""
        return check_password_hash(self.senha_hash, senha)
    
    def get_id(self):
        """Retorna o ID para o Flask-Login."""
        return f"admin:{self.id}"
    
    @property
    def tipo_usuario(self):
        return 'admin'
    
    def __repr__(self):
        return f'<Admin {self.nome}>'
