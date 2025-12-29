from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, FloatField, DateField, TimeField
from wtforms.validators import DataRequired, Length, Optional, NumberRange

from app.models.trabalho import Trabalho


class TrabalhoForm(FlaskForm):
    """Formulário de criação/edição de trabalho."""
    
    titulo = StringField('Título do trabalho', validators=[
        DataRequired(message='Título é obrigatório'),
        Length(min=5, max=200, message='Título deve ter entre 5 e 200 caracteres')
    ])
    descricao = TextAreaField('Descrição do serviço', validators=[
        DataRequired(message='Descrição é obrigatória'),
        Length(min=20, message='Descreva melhor o trabalho (mínimo 20 caracteres)')
    ])
    categoria = SelectField('Categoria', choices=[
        ('garcom', 'Garçom'),
        ('bartender', 'Bartender'),
        ('organizacao', 'Organização de Eventos')
    ], validators=[DataRequired()])
    requisitos = TextAreaField('Requisitos (ex: roupa social, experiência)', validators=[
        Optional(),
        Length(max=500)
    ])
    local_endereco = StringField('Endereço do evento', validators=[
        DataRequired(message='Endereço é obrigatório'),
        Length(max=300)
    ])
    local_cidade = StringField('Cidade', validators=[
        DataRequired(message='Cidade é obrigatória'),
        Length(max=100)
    ])
    data = DateField('Data do trabalho', validators=[
        DataRequired(message='Data é obrigatória')
    ], format='%Y-%m-%d')
    horario_inicio = TimeField('Horário de início', validators=[
        DataRequired(message='Horário de início é obrigatório')
    ], format='%H:%M')
    horario_fim = TimeField('Horário de término', validators=[
        DataRequired(message='Horário de término é obrigatório')
    ], format='%H:%M')
    valor_pagamento = FloatField('Valor por pessoa (R$)', validators=[
        DataRequired(message='Valor é obrigatório'),
        NumberRange(min=1, message='Valor deve ser maior que zero')
    ])
    vagas_total = IntegerField('Quantidade de pessoas', validators=[
        DataRequired(message='Quantidade é obrigatória'),
        NumberRange(min=1, max=50, message='Quantidade deve ser entre 1 e 50')
    ])


class EditarEmpresaForm(FlaskForm):
    """Formulário de edição de perfil da empresa."""
    
    nome_fantasia = StringField('Nome Fantasia', validators=[
        DataRequired(message='Nome fantasia é obrigatório'),
        Length(max=200)
    ])
    telefone = StringField('Telefone', validators=[
        DataRequired(message='Telefone é obrigatório'),
        Length(min=10, max=20)
    ])
    pessoa_contato = StringField('Pessoa de contato', validators=[
        DataRequired(message='Pessoa de contato é obrigatória'),
        Length(max=150)
    ])
    endereco_rua = StringField('Endereço', validators=[
        DataRequired(message='Endereço é obrigatório'),
        Length(max=200)
    ])
    endereco_cidade = StringField('Cidade', validators=[
        DataRequired(message='Cidade é obrigatória'),
        Length(max=100)
    ])
    endereco_estado = SelectField('Estado', choices=[
        ('PR', 'Paraná'), ('SC', 'Santa Catarina'), ('RS', 'Rio Grande do Sul'),
        ('SP', 'São Paulo'), ('RJ', 'Rio de Janeiro'), ('MG', 'Minas Gerais'),
        ('MS', 'Mato Grosso do Sul'), ('MT', 'Mato Grosso'), ('GO', 'Goiás'),
        ('DF', 'Distrito Federal'), ('BA', 'Bahia'), ('ES', 'Espírito Santo'),
        ('PE', 'Pernambuco'), ('CE', 'Ceará'), ('PA', 'Pará'), ('AM', 'Amazonas'),
        ('MA', 'Maranhão'), ('PB', 'Paraíba'), ('RN', 'Rio Grande do Norte'),
        ('PI', 'Piauí'), ('AL', 'Alagoas'), ('SE', 'Sergipe'), ('TO', 'Tocantins'),
        ('RO', 'Rondônia'), ('AC', 'Acre'), ('AP', 'Amapá'), ('RR', 'Roraima')
    ], validators=[DataRequired()])
    endereco_cep = StringField('CEP', validators=[
        DataRequired(message='CEP é obrigatório'),
        Length(min=8, max=10)
    ])
