from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from app import db
from app.models import Colaborador, Empresa, Admin
from app.forms.auth import (
    LoginForm, 
    CadastroColaboradorForm, 
    CadastroEmpresaForm,
    LoginAdminForm
)
from app.utils.upload import salvar_imagem
from app.utils.email import email_boas_vindas_colaborador, email_boas_vindas_empresa

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login de colaborador ou empresa - detecta automaticamente o tipo."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        email = form.email.data.lower()
        senha = form.senha.data
        
        # Tenta encontrar o usuário como colaborador primeiro, depois como empresa
        user = Colaborador.query.filter_by(email=email).first()
        tipo = 'colaborador'
        
        if not user:
            user = Empresa.query.filter_by(email=email).first()
            tipo = 'empresa'
        
        if user and user.check_senha(senha):
            if hasattr(user, 'status') and user.status == 'suspenso':
                flash('Sua conta está suspensa. Entre em contato com o suporte.', 'danger')
                return redirect(url_for('auth.login'))
            
            login_user(user)    
            nome_exibir = user.nome if tipo == 'colaborador' else user.nome_fantasia
            flash(f'Bem-vindo(a), {nome_exibir}!', 'success')
            
            next_page = request.args.get('next')
            if tipo == 'colaborador':
                return redirect(next_page or url_for('colaborador.dashboard'))
            else:
                return redirect(next_page or url_for('empresa.dashboard'))
        else:
            flash('Email ou senha incorretos.', 'danger')
    
    return render_template('auth/login.html', form=form)


@auth_bp.route('/cadastro/colaborador', methods=['GET', 'POST'])
def cadastro_colaborador():
    """Cadastro de novo colaborador."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = CadastroColaboradorForm()
    
    if form.validate_on_submit():
        # Salva foto de perfil
        foto_filename = salvar_imagem(form.foto_perfil.data, 'perfil')
        
        colaborador = Colaborador(
            nome=form.nome.data,
            email=form.email.data.lower(),
            telefone=form.telefone.data,
            universidade=form.universidade.data,
            foto_perfil=foto_filename,
            bio=form.bio.data,
            habilidades=form.habilidades.data
        )
        colaborador.set_senha(form.senha.data)
        
        db.session.add(colaborador)
        db.session.commit()
        
        # Envia email de boas-vindas
        email_boas_vindas_colaborador(colaborador.nome, colaborador.email)
        
        flash('Cadastro realizado com sucesso! Faça login para continuar.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/cadastro_colaborador.html', form=form)


@auth_bp.route('/cadastro/empresa', methods=['GET', 'POST'])
def cadastro_empresa():
    """Cadastro de nova empresa."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = CadastroEmpresaForm()
    
    if form.validate_on_submit():
        # Salva logo se enviada
        logo_filename = None
        if form.logo.data:
            logo_filename = salvar_imagem(form.logo.data, 'empresas')
        
        empresa = Empresa(
            email=form.email.data.lower(),
            razao_social=form.razao_social.data,
            nome_fantasia=form.nome_fantasia.data,
            cnpj=form.cnpj.data,
            telefone=form.telefone.data,
            pessoa_contato=form.pessoa_contato.data,
            endereco_rua=form.endereco_rua.data,
            endereco_cidade=form.endereco_cidade.data,
            endereco_estado=form.endereco_estado.data,
            endereco_cep=form.endereco_cep.data,
            logo=logo_filename,
            status='aguardando_aprovacao'
        )
        empresa.set_senha(form.senha.data)
        
        db.session.add(empresa)
        db.session.commit()
        
        # Envia email de boas-vindas
        email_boas_vindas_empresa(empresa.nome_fantasia, empresa.email)
        
        flash('Cadastro enviado! Aguarde a aprovação do administrador para publicar trabalhos.', 'info')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/cadastro_empresa.html', form=form)


@auth_bp.route('/admin/login', methods=['GET', 'POST'])
def login_admin():
    """Login do administrador."""
    if current_user.is_authenticated and current_user.tipo_usuario == 'admin':
        return redirect(url_for('admin.dashboard'))
    
    form = LoginAdminForm()
    
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.email.data.lower()).first()
        
        if admin and admin.check_senha(form.senha.data):
            login_user(admin)
            flash('Bem-vindo ao painel administrativo!', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Credenciais inválidas.', 'danger')
    
    return render_template('auth/login_admin.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    """Logout do usuário."""
    logout_user()
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('main.index'))
