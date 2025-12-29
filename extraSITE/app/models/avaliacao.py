import uuid
from datetime import datetime

from app import db


class Avaliacao(db.Model):
    """Modelo de Avaliação entre Empresa e Colaborador."""
    
    __tablename__ = 'avaliacoes'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Referências
    candidatura_id = db.Column(db.String(36), db.ForeignKey('candidaturas.id'), nullable=False)
    trabalho_id = db.Column(db.String(36), db.ForeignKey('trabalhos.id'), nullable=False)
    
    # Quem avalia quem
    avaliador_tipo = db.Column(db.String(20), nullable=False)  # 'empresa' ou 'colaborador'
    avaliador_id = db.Column(db.String(36), nullable=False)
    avaliado_tipo = db.Column(db.String(20), nullable=False)  # 'empresa' ou 'colaborador'
    avaliado_id = db.Column(db.String(36), nullable=False)
    
    # Avaliação
    nota = db.Column(db.Integer, nullable=False)  # 1 a 5 estrelas
    comentario = db.Column(db.Text, nullable=True)
    
    # Categorias específicas (opcionais)
    pontualidade = db.Column(db.Integer, nullable=True)  # 1-5
    profissionalismo = db.Column(db.Integer, nullable=True)  # 1-5
    comunicacao = db.Column(db.Integer, nullable=True)  # 1-5
    
    # Timestamp
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    candidatura = db.relationship('Candidatura', backref=db.backref('avaliacoes', lazy='dynamic'))
    trabalho = db.relationship('Trabalho', backref=db.backref('avaliacoes', lazy='dynamic'))
    
    # Índice único para evitar avaliações duplicadas
    __table_args__ = (
        db.UniqueConstraint('candidatura_id', 'avaliador_tipo', name='uq_avaliacao_candidatura_avaliador'),
    )
    
    @property
    def avaliador(self):
        """Retorna o objeto do avaliador."""
        if self.avaliador_tipo == 'empresa':
            from app.models.empresa import Empresa
            return Empresa.query.get(self.avaliador_id)
        else:
            from app.models.colaborador import Colaborador
            return Colaborador.query.get(self.avaliador_id)
    
    @property
    def avaliado(self):
        """Retorna o objeto do avaliado."""
        if self.avaliado_tipo == 'empresa':
            from app.models.empresa import Empresa
            return Empresa.query.get(self.avaliado_id)
        else:
            from app.models.colaborador import Colaborador
            return Colaborador.query.get(self.avaliado_id)
    
    @staticmethod
    def empresa_ja_avaliou(candidatura_id):
        """Verifica se empresa já avaliou o colaborador nesta candidatura."""
        return Avaliacao.query.filter_by(
            candidatura_id=candidatura_id,
            avaliador_tipo='empresa'
        ).first() is not None
    
    @staticmethod
    def colaborador_ja_avaliou(candidatura_id):
        """Verifica se colaborador já avaliou a empresa nesta candidatura."""
        return Avaliacao.query.filter_by(
            candidatura_id=candidatura_id,
            avaliador_tipo='colaborador'
        ).first() is not None
    
    @staticmethod
    def criar_avaliacao_empresa(candidatura, nota, comentario=None, pontualidade=None, profissionalismo=None, comunicacao=None):
        """Empresa avalia o colaborador."""
        avaliacao = Avaliacao(
            candidatura_id=candidatura.id,
            trabalho_id=candidatura.trabalho_id,
            avaliador_tipo='empresa',
            avaliador_id=candidatura.trabalho.empresa_id,
            avaliado_tipo='colaborador',
            avaliado_id=candidatura.colaborador_id,
            nota=nota,
            comentario=comentario,
            pontualidade=pontualidade,
            profissionalismo=profissionalismo,
            comunicacao=comunicacao
        )
        
        db.session.add(avaliacao)
        
        # Atualiza média do colaborador
        colaborador = candidatura.colaborador
        colaborador.total_avaliacoes += 1
        
        # Recalcula média
        todas_avaliacoes = Avaliacao.query.filter_by(
            avaliado_tipo='colaborador',
            avaliado_id=colaborador.id
        ).all()
        
        soma = sum(a.nota for a in todas_avaliacoes) + nota
        colaborador.avaliacao_media = soma / (len(todas_avaliacoes) + 1)
        
        return avaliacao
    
    @staticmethod
    def criar_avaliacao_colaborador(candidatura, nota, comentario=None, pontualidade=None, profissionalismo=None, comunicacao=None):
        """Colaborador avalia a empresa."""
        avaliacao = Avaliacao(
            candidatura_id=candidatura.id,
            trabalho_id=candidatura.trabalho_id,
            avaliador_tipo='colaborador',
            avaliador_id=candidatura.colaborador_id,
            avaliado_tipo='empresa',
            avaliado_id=candidatura.trabalho.empresa_id,
            nota=nota,
            comentario=comentario,
            pontualidade=pontualidade,
            profissionalismo=profissionalismo,
            comunicacao=comunicacao
        )
        
        db.session.add(avaliacao)
        
        # Atualiza média da empresa
        from app.models.empresa import Empresa
        empresa = candidatura.trabalho.empresa
        empresa.total_avaliacoes += 1
        
        # Recalcula média
        todas_avaliacoes = Avaliacao.query.filter_by(
            avaliado_tipo='empresa',
            avaliado_id=empresa.id
        ).all()
        
        soma = sum(a.nota for a in todas_avaliacoes) + nota
        empresa.avaliacao_media = soma / (len(todas_avaliacoes) + 1)
        
        return avaliacao
    
    def __repr__(self):
        return f'<Avaliacao {self.avaliador_tipo}:{self.avaliador_id} -> {self.avaliado_tipo}:{self.avaliado_id} = {self.nota}>'
