import uuid
from datetime import datetime, date, time

from flask import current_app
from app import db


class Trabalho(db.Model):
    """Modelo do Trabalho (Gig)."""
    
    __tablename__ = 'trabalhos'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    empresa_id = db.Column(db.String(36), db.ForeignKey('empresas.id'), nullable=False)
    
    # Informações do trabalho
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    categoria = db.Column(db.String(50), nullable=False)  # garcom, bartender, organizacao
    requisitos = db.Column(db.Text, nullable=True)
    
    # Local
    local_endereco = db.Column(db.String(300), nullable=False)
    local_cidade = db.Column(db.String(100), nullable=False)
    
    # Data e horário
    data = db.Column(db.Date, nullable=False)
    horario_inicio = db.Column(db.Time, nullable=False)
    horario_fim = db.Column(db.Time, nullable=False)
    
    # Valores
    valor_pagamento = db.Column(db.Float, nullable=False)  # Por colaborador
    valor_sugerido = db.Column(db.Float, nullable=True)    # Referência da plataforma
    
    # Vagas
    vagas_total = db.Column(db.Integer, nullable=False, default=1)
    vagas_preenchidas = db.Column(db.Integer, default=0)
    
    # Status
    status = db.Column(db.String(20), default='aberto')  # rascunho, aberto, em_andamento, concluido, cancelado
    
    # Timestamps
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    candidaturas = db.relationship('Candidatura', backref='trabalho', lazy='dynamic')
    
    # Categorias disponíveis
    CATEGORIAS = {
        'garcom': 'Garçom',
        'bartender': 'Bartender',
        'organizacao': 'Organização de Eventos'
    }
    
    # Valores sugeridos por categoria (por hora) - fallback se não configurado
    VALORES_SUGERIDOS_DEFAULT = {
        'garcom': 15.0,
        'bartender': 20.0,
        'organizacao': 18.0
    }
    
    @property
    def categoria_display(self):
        """Retorna o nome da categoria formatado."""
        return self.CATEGORIAS.get(self.categoria, self.categoria)
    
    @property
    def duracao_horas(self):
        """Calcula a duração em horas."""
        inicio = datetime.combine(date.today(), self.horario_inicio)
        fim = datetime.combine(date.today(), self.horario_fim)
        delta = fim - inicio
        return delta.seconds / 3600
    
    @property
    def valor_total(self):
        """Calcula o valor total (todas as vagas)."""
        return self.valor_pagamento * self.vagas_total
    
    @property
    def valor_liquido(self):
        """Calcula o valor líquido que o colaborador recebe (menos taxa da plataforma)."""
        taxa = current_app.config.get('TAKE_RATE', 0.15)
        return self.valor_pagamento * (1 - taxa)
    
    @property
    def taxa_plataforma(self):
        """Retorna o valor da taxa da plataforma."""
        taxa = current_app.config.get('TAKE_RATE', 0.15)
        return self.valor_pagamento * taxa
    
    @property
    def vagas_disponiveis(self):
        """Retorna quantas vagas ainda estão disponíveis."""
        return self.vagas_total - self.vagas_preenchidas
    
    @property
    def esta_aberto(self):
        """Verifica se o trabalho está aceitando candidaturas."""
        return self.status == 'aberto' and self.vagas_disponiveis > 0
    
    def calcular_valor_sugerido(self):
        """Calcula o valor sugerido baseado na categoria e duração."""
        valores_config = current_app.config.get('VALORES_SUGERIDOS', self.VALORES_SUGERIDOS_DEFAULT)
        valor_hora = valores_config.get(self.categoria, 15.0)
        self.valor_sugerido = valor_hora * self.duracao_horas
        return self.valor_sugerido
    
    def __repr__(self):
        return f'<Trabalho {self.titulo}>'
