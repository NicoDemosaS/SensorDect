from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional


class EditarPerfilForm(FlaskForm):
    """Formulário de edição de perfil do colaborador."""
    
    nome = StringField('Nome completo', validators=[
        DataRequired(message='Nome é obrigatório'),
        Length(min=3, max=150)
    ])
    telefone = StringField('Telefone (WhatsApp)', validators=[
        DataRequired(message='Telefone é obrigatório'),
        Length(min=10, max=20)
    ])
    universidade = StringField('Universidade', validators=[
        Optional(),
        Length(max=150)
    ])
    bio = TextAreaField('Sobre você', validators=[
        Optional(),
        Length(max=500)
    ])
    habilidades = TextAreaField('Habilidades e experiências', validators=[
        Optional(),
        Length(max=1000)
    ])
    chave_pix = StringField('Chave PIX (para receber pagamentos)', validators=[
        Optional(),
        Length(max=100)
    ])


class CandidaturaForm(FlaskForm):
    """Formulário de candidatura a um trabalho."""
    
    mensagem = TextAreaField('Mensagem para a empresa (opcional)', validators=[
        Optional(),
        Length(max=500, message='Mensagem muito longa (máx 500 caracteres)')
    ])
