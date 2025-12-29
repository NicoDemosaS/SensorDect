import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db


class Empresa(UserMixin, db.Model):
    """Modelo da Empresa."""
    
    __tablename__ = 'empresas'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Dados obrigatórios
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    senha_hash = db.Column(db.String(256), nullable=False)
    razao_social = db.Column(db.String(200), nullable=False)
    nome_fantasia = db.Column(db.String(200), nullable=False)
    cnpj = db.Column(db.String(18), unique=True, nullable=False, index=True)  # XX.XXX.XXX/XXXX-XX
    telefone = db.Column(db.String(20), nullable=False)
    pessoa_contato = db.Column(db.String(150), nullable=False)
    
    # Endereço
    endereco_rua = db.Column(db.String(200), nullable=False)
    endereco_cidade = db.Column(db.String(100), nullable=False)
    endereco_estado = db.Column(db.String(2), nullable=False)
    endereco_cep = db.Column(db.String(10), nullable=False)
    
    # Dados opcionais
    logo = db.Column(db.String(255), nullable=True)
    
    # Status e aprovação
    status = db.Column(db.String(30), default='aguardando_aprovacao')  # aguardando_aprovacao, ativo, suspenso
    aprovado_por = db.Column(db.String(36), db.ForeignKey('admins.id'), nullable=True)
    aprovado_em = db.Column(db.DateTime, nullable=True)
    motivo_rejeicao = db.Column(db.Text, nullable=True)
    
    # Avaliação (para futuro)
    avaliacao_media = db.Column(db.Float, default=0.0)
    total_avaliacoes = db.Column(db.Integer, default=0)
    total_trabalhos = db.Column(db.Integer, default=0)
    
    # Timestamps
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    trabalhos = db.relationship('Trabalho', backref='empresa', lazy='dynamic')
    
    def set_senha(self, senha):
        """Define a senha da empresa (hash)."""
        self.senha_hash = generate_password_hash(senha)
    
    def check_senha(self, senha):
        """Verifica se a senha está correta."""
        return check_password_hash(self.senha_hash, senha)
    
    def get_id(self):
        """Retorna o ID para o Flask-Login."""
        return f"empresa:{self.id}"
    
    @property
    def tipo_usuario(self):
        return 'empresa'
    
    @property
    def pode_publicar(self):
        """Verifica se a empresa pode publicar trabalhos."""
        return self.status == 'ativo'
    
    @property
    def endereco_completo(self):
        """Retorna o endereço formatado."""
        return f"{self.endereco_rua}, {self.endereco_cidade}/{self.endereco_estado} - CEP: {self.endereco_cep}"
    
    def __repr__(self):
        return f'<Empresa {self.nome_fantasia}>'
