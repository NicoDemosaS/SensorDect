from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Optional

from app.models import Colaborador, Empresa


class LoginForm(FlaskForm):
    """Formulário de login."""
    
    email = StringField('Email', validators=[
        DataRequired(message='Email é obrigatório'),
        Email(message='Email inválido')
    ])
    senha = PasswordField('Senha', validators=[
        DataRequired(message='Senha é obrigatória')
    ])


class CadastroColaboradorForm(FlaskForm):
    """Formulário de cadastro de colaborador."""
    
    nome = StringField('Nome completo', validators=[
        DataRequired(message='Nome é obrigatório'),
        Length(min=3, max=150, message='Nome deve ter entre 3 e 150 caracteres')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='Email é obrigatório'),
        Email(message='Email inválido')
    ])
    telefone = StringField('Telefone (WhatsApp)', validators=[
        DataRequired(message='Telefone é obrigatório'),
        Length(min=10, max=20, message='Telefone inválido')
    ])
    universidade = StringField('Universidade', validators=[
        DataRequired(message='Universidade é obrigatória'),
        Length(max=150)
    ])
    foto_perfil = FileField('Foto de perfil', validators=[
        FileRequired(message='Foto de perfil é obrigatória'),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Apenas imagens são permitidas')
    ])
    bio = TextAreaField('Sobre você (opcional)', validators=[
        Optional(),
        Length(max=500)
    ])
    habilidades = TextAreaField('Habilidades e experiências (opcional)', validators=[
        Optional(),
        Length(max=1000)
    ])
    senha = PasswordField('Senha', validators=[
        DataRequired(message='Senha é obrigatória'),
        Length(min=6, message='Senha deve ter no mínimo 6 caracteres')
    ])
    confirmar_senha = PasswordField('Confirmar senha', validators=[
        DataRequired(message='Confirme sua senha'),
        EqualTo('senha', message='Senhas não conferem')
    ])
    
    def validate_email(self, field):
        """Verifica se o email já está cadastrado."""
        if Colaborador.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Este email já está cadastrado.')


class CadastroEmpresaForm(FlaskForm):
    """Formulário de cadastro de empresa."""
    
    email = StringField('Email', validators=[
        DataRequired(message='Email é obrigatório'),
        Email(message='Email inválido')
    ])
    razao_social = StringField('Razão Social', validators=[
        DataRequired(message='Razão social é obrigatória'),
        Length(max=200)
    ])
    nome_fantasia = StringField('Nome Fantasia', validators=[
        DataRequired(message='Nome fantasia é obrigatório'),
        Length(max=200)
    ])
    cnpj = StringField('CNPJ', validators=[
        DataRequired(message='CNPJ é obrigatório'),
        Length(min=14, max=18, message='CNPJ inválido')
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
    logo = FileField('Logo da empresa (opcional)', validators=[
        Optional(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Apenas imagens são permitidas')
    ])
    senha = PasswordField('Senha', validators=[
        DataRequired(message='Senha é obrigatória'),
        Length(min=6, message='Senha deve ter no mínimo 6 caracteres')
    ])
    confirmar_senha = PasswordField('Confirmar senha', validators=[
        DataRequired(message='Confirme sua senha'),
        EqualTo('senha', message='Senhas não conferem')
    ])
    
    def validate_email(self, field):
        """Verifica se o email já está cadastrado."""
        if Empresa.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Este email já está cadastrado.')
    
    def validate_cnpj(self, field):
        """Verifica se o CNPJ já está cadastrado."""
        cnpj_limpo = ''.join(filter(str.isdigit, field.data))
        if Empresa.query.filter_by(cnpj=field.data).first():
            raise ValidationError('Este CNPJ já está cadastrado.')


class LoginAdminForm(FlaskForm):
    """Formulário de login do admin."""
    
    email = StringField('Email', validators=[
        DataRequired(message='Email é obrigatório'),
        Email(message='Email inválido')
    ])
    senha = PasswordField('Senha', validators=[
        DataRequired(message='Senha é obrigatória')
    ])
