import uuid
from datetime import datetime

from app import db


class Candidatura(db.Model):
    """Modelo da Candidatura."""
    
    __tablename__ = 'candidaturas'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    trabalho_id = db.Column(db.String(36), db.ForeignKey('trabalhos.id'), nullable=False)
    colaborador_id = db.Column(db.String(36), db.ForeignKey('colaboradores.id'), nullable=False)
    
    # Mensagem opcional do colaborador
    mensagem = db.Column(db.Text, nullable=True)
    
    # Status da candidatura
    status = db.Column(db.String(20), default='pendente')  # pendente, aceita, recusada, cancelada
    
    # Confirmação de execução
    confirmado_empresa = db.Column(db.Boolean, default=False)  # Empresa confirmou que compareceu
    compareceu = db.Column(db.Boolean, nullable=True)  # True = foi, False = faltou, None = não avaliado
    
    # Timestamps
    candidatou_em = db.Column(db.DateTime, default=datetime.utcnow)
    respondido_em = db.Column(db.DateTime, nullable=True)
    
    # Índice único para evitar candidaturas duplicadas
    __table_args__ = (
        db.UniqueConstraint('trabalho_id', 'colaborador_id', name='uq_candidatura_trabalho_colaborador'),
    )
    
    @property
    def foi_aceita(self):
        return self.status == 'aceita'
    
    @property
    def esta_pendente(self):
        return self.status == 'pendente'
    
    def aceitar(self):
        """Aceita a candidatura e atualiza vagas do trabalho."""
        if self.status == 'pendente':
            self.status = 'aceita'
            self.respondido_em = datetime.utcnow()
            self.trabalho.vagas_preenchidas += 1
            
            # Cancela outras candidaturas conflitantes do mesmo colaborador
            self._cancelar_conflitantes()
    
    def recusar(self):
        """Recusa a candidatura."""
        if self.status == 'pendente':
            self.status = 'recusada'
            self.respondido_em = datetime.utcnow()
    
    def cancelar(self):
        """Cancela a candidatura (pelo colaborador)."""
        if self.status in ['pendente', 'aceita']:
            if self.status == 'aceita':
                self.trabalho.vagas_preenchidas -= 1
            self.status = 'cancelada'
            self.respondido_em = datetime.utcnow()
    
    def _cancelar_conflitantes(self):
        """Cancela candidaturas do mesmo colaborador que conflitam no horário."""
        from app.models.trabalho import Trabalho
        
        trabalho_aceito = self.trabalho
        
        # Busca outras candidaturas pendentes do colaborador
        outras = Candidatura.query.filter(
            Candidatura.colaborador_id == self.colaborador_id,
            Candidatura.id != self.id,
            Candidatura.status == 'pendente'
        ).all()
        
        for candidatura in outras:
            outro_trabalho = candidatura.trabalho
            
            # Verifica se é no mesmo dia
            if outro_trabalho.data == trabalho_aceito.data:
                # Verifica conflito de horário
                if self._horarios_conflitam(trabalho_aceito, outro_trabalho):
                    candidatura.status = 'cancelada'
                    candidatura.respondido_em = datetime.utcnow()
    
    def _horarios_conflitam(self, t1, t2):
        """Verifica se dois trabalhos têm horários conflitantes."""
        # Trabalho 1 começa antes de trabalho 2 terminar E
        # Trabalho 1 termina depois de trabalho 2 começar
        return t1.horario_inicio < t2.horario_fim and t1.horario_fim > t2.horario_inicio
    
    def __repr__(self):
        return f'<Candidatura {self.colaborador_id} -> {self.trabalho_id}>'
