import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db, login_manager


class Colaborador(UserMixin, db.Model):
    """Modelo do Colaborador (Estudante Universitário)."""
    
    __tablename__ = 'colaboradores'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Dados obrigatórios
    nome = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    senha_hash = db.Column(db.String(256), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    universidade = db.Column(db.String(150), nullable=False)
    foto_perfil = db.Column(db.String(255), nullable=False)  # URL/path da foto
    
    # Dados opcionais
    bio = db.Column(db.Text, nullable=True)
    habilidades = db.Column(db.Text, nullable=True)  # Texto livre
    experiencias = db.Column(db.JSON, nullable=True)  # Lista de experiências
    chave_pix = db.Column(db.String(100), nullable=True)
    
    # Status e controle
    status = db.Column(db.String(20), default='ativo')  # pendente, ativo, suspenso
    email_verificado = db.Column(db.Boolean, default=False)
    
    # Avaliação (para futuro)
    avaliacao_media = db.Column(db.Float, default=0.0)
    total_avaliacoes = db.Column(db.Integer, default=0)
    total_trabalhos = db.Column(db.Integer, default=0)
    
    # Timestamps
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    candidaturas = db.relationship('Candidatura', backref='colaborador', lazy='dynamic')
    
    def set_senha(self, senha):
        """Define a senha do colaborador (hash)."""
        self.senha_hash = generate_password_hash(senha)
    
    def check_senha(self, senha):
        """Verifica se a senha está correta."""
        return check_password_hash(self.senha_hash, senha)
    
    def get_id(self):
        """Retorna o ID para o Flask-Login."""
        return f"colaborador:{self.id}"
    
    @property
    def tipo_usuario(self):
        return 'colaborador'
    
    def __repr__(self):
        return f'<Colaborador {self.nome}>'


@login_manager.user_loader
def load_user(user_id):
    """Carrega usuário pelo ID (usado pelo Flask-Login)."""
    if ':' in user_id:
        tipo, id = user_id.split(':', 1)
        if tipo == 'colaborador':
            return Colaborador.query.get(id)
        elif tipo == 'empresa':
            from app.models.empresa import Empresa
            return Empresa.query.get(id)
        elif tipo == 'admin':
            from app.models.admin import Admin
            return Admin.query.get(id)
    return None
