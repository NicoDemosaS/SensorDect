from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from functools import wraps
from datetime import datetime
import json
import os

from app import db
from app.models import Empresa, Colaborador, Trabalho, Admin
from app.utils.email import email_empresa_aprovada

admin_bp = Blueprint('admin', __name__)


def admin_required(f):
    """Decorator que exige que o usuário seja um admin."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.tipo_usuario != 'admin':
            flash('Acesso restrito a administradores.', 'danger')
            return redirect(url_for('auth.login_admin'))
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Dashboard do administrador."""
    # Contadores
    empresas_pendentes = Empresa.query.filter_by(status='aguardando_aprovacao').count()
    empresas_ativas = Empresa.query.filter_by(status='ativo').count()
    total_colaboradores = Colaborador.query.count()
    total_trabalhos = Trabalho.query.count()
    trabalhos_abertos = Trabalho.query.filter_by(status='aberto').count()
    
    # Empresas aguardando aprovação
    pendentes = Empresa.query.filter_by(status='aguardando_aprovacao').order_by(
        Empresa.criado_em.asc()
    ).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         empresas_pendentes=empresas_pendentes,
                         empresas_ativas=empresas_ativas,
                         total_colaboradores=total_colaboradores,
                         total_trabalhos=total_trabalhos,
                         trabalhos_abertos=trabalhos_abertos,
                         pendentes=pendentes)


@admin_bp.route('/empresas')
@login_required
@admin_required
def listar_empresas():
    """Lista todas as empresas."""
    status_filtro = request.args.get('status', '')
    
    query = Empresa.query
    
    if status_filtro:
        query = query.filter_by(status=status_filtro)
    
    empresas = query.order_by(Empresa.criado_em.desc()).all()
    
    return render_template('admin/empresas.html',
                         empresas=empresas,
                         filtro=status_filtro)


@admin_bp.route('/empresa/<empresa_id>')
@login_required
@admin_required
def ver_empresa(empresa_id):
    """Ver detalhes de uma empresa."""
    empresa = Empresa.query.get_or_404(empresa_id)
    return render_template('admin/empresa_detalhe.html', empresa=empresa)


@admin_bp.route('/empresa/<empresa_id>/aprovar', methods=['POST'])
@login_required
@admin_required
def aprovar_empresa(empresa_id):
    """Aprova uma empresa."""
    empresa = Empresa.query.get_or_404(empresa_id)
    
    empresa.status = 'ativo'
    empresa.aprovado_por = current_user.id
    empresa.aprovado_em = datetime.utcnow()
    
    db.session.commit()
    
    # Envia email notificando a empresa
    email_empresa_aprovada(empresa.nome_fantasia, empresa.email)
    
    flash(f'Empresa {empresa.nome_fantasia} aprovada com sucesso!', 'success')
    return redirect(url_for('admin.listar_empresas', status='aguardando_aprovacao'))


@admin_bp.route('/empresa/<empresa_id>/rejeitar', methods=['POST'])
@login_required
@admin_required
def rejeitar_empresa(empresa_id):
    """Rejeita uma empresa."""
    empresa = Empresa.query.get_or_404(empresa_id)
    motivo = request.form.get('motivo', 'Não informado')
    
    empresa.status = 'suspenso'
    empresa.motivo_rejeicao = motivo
    
    db.session.commit()
    
    flash(f'Empresa {empresa.nome_fantasia} rejeitada.', 'warning')
    return redirect(url_for('admin.listar_empresas'))


@admin_bp.route('/empresa/<empresa_id>/suspender', methods=['POST'])
@login_required
@admin_required
def suspender_empresa(empresa_id):
    """Suspende uma empresa."""
    empresa = Empresa.query.get_or_404(empresa_id)
    motivo = request.form.get('motivo', 'Não informado')
    
    empresa.status = 'suspenso'
    empresa.motivo_rejeicao = motivo
    
    db.session.commit()
    
    flash(f'Empresa {empresa.nome_fantasia} suspensa.', 'warning')
    return redirect(url_for('admin.ver_empresa', empresa_id=empresa_id))


@admin_bp.route('/colaboradores')
@login_required
@admin_required
def listar_colaboradores():
    """Lista todos os colaboradores."""
    colaboradores = Colaborador.query.order_by(Colaborador.criado_em.desc()).all()
    return render_template('admin/colaboradores.html', colaboradores=colaboradores)


@admin_bp.route('/colaborador/<colaborador_id>')
@login_required
@admin_required
def ver_colaborador(colaborador_id):
    """Ver detalhes de um colaborador."""
    colaborador = Colaborador.query.get_or_404(colaborador_id)
    return render_template('admin/colaborador_detalhe.html', colaborador=colaborador)


@admin_bp.route('/colaborador/<colaborador_id>/suspender', methods=['POST'])
@login_required
@admin_required
def suspender_colaborador(colaborador_id):
    """Suspende um colaborador."""
    colaborador = Colaborador.query.get_or_404(colaborador_id)
    
    colaborador.status = 'suspenso'
    db.session.commit()
    
    flash(f'Colaborador {colaborador.nome} suspenso.', 'warning')
    return redirect(url_for('admin.ver_colaborador', colaborador_id=colaborador_id))


@admin_bp.route('/colaborador/<colaborador_id>/ativar', methods=['POST'])
@login_required
@admin_required
def ativar_colaborador(colaborador_id):
    """Ativa um colaborador suspenso."""
    colaborador = Colaborador.query.get_or_404(colaborador_id)
    
    colaborador.status = 'ativo'
    db.session.commit()
    
    flash(f'Colaborador {colaborador.nome} ativado.', 'success')
    return redirect(url_for('admin.ver_colaborador', colaborador_id=colaborador_id))


@admin_bp.route('/trabalhos')
@login_required
@admin_required
def listar_trabalhos():
    """Lista todos os trabalhos."""
    status_filtro = request.args.get('status', '')
    
    query = Trabalho.query
    
    if status_filtro:
        query = query.filter_by(status=status_filtro)
    
    trabalhos = query.order_by(Trabalho.criado_em.desc()).all()
    
    return render_template('admin/trabalhos.html',
                         trabalhos=trabalhos,
                         filtro=status_filtro)


@admin_bp.route('/trabalho/<trabalho_id>/cancelar', methods=['POST'])
@login_required
@admin_required
def cancelar_trabalho(trabalho_id):
    """Cancela um trabalho (admin)."""
    trabalho = Trabalho.query.get_or_404(trabalho_id)
    
    trabalho.status = 'cancelado'
    db.session.commit()
    
    flash(f'Trabalho "{trabalho.titulo}" cancelado.', 'warning')
    return redirect(url_for('admin.listar_trabalhos'))


def get_config_file_path():
    """Retorna o caminho do arquivo de configurações."""
    return os.path.join(current_app.instance_path, 'platform_config.json')


def load_platform_config():
    """Carrega configurações da plataforma do arquivo JSON."""
    config_path = get_config_file_path()
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return json.load(f)
    return {}


def save_platform_config(config_data):
    """Salva configurações da plataforma no arquivo JSON."""
    config_path = get_config_file_path()
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, 'w') as f:
        json.dump(config_data, f, indent=2)


@admin_bp.route('/configuracoes', methods=['GET', 'POST'])
@login_required
@admin_required
def configuracoes():
    """Página de configurações da plataforma."""
    if request.method == 'POST':
        config_data = load_platform_config()
        form_type = request.form.get('form_type')
        
        try:
            if form_type == 'geral':
                # Configurações gerais
                config_data['PLATFORM_NAME'] = request.form.get('platform_name', 'ExtraSITE').strip()
                config_data['PLATFORM_CITY'] = request.form.get('platform_city', 'Medianeira - PR').strip()
                
                current_app.config['PLATFORM_NAME'] = config_data['PLATFORM_NAME']
                current_app.config['PLATFORM_CITY'] = config_data['PLATFORM_CITY']
                
                flash('Configurações gerais atualizadas!', 'success')
                
            elif form_type == 'taxa':
                # Taxa da plataforma
                taxa = float(request.form.get('take_rate', 15)) / 100
                if taxa < 0 or taxa > 1:
                    flash('Taxa deve estar entre 0% e 100%.', 'danger')
                    return redirect(url_for('admin.configuracoes'))
                
                config_data['TAKE_RATE'] = taxa
                current_app.config['TAKE_RATE'] = taxa
                
                flash(f'Taxa da plataforma atualizada para {int(taxa * 100)}%!', 'success')
                
            elif form_type == 'cancelamento':
                # Janela de cancelamento
                horas = int(request.form.get('cancellation_hours', 48))
                if horas < 0:
                    flash('Janela de cancelamento deve ser positiva.', 'danger')
                    return redirect(url_for('admin.configuracoes'))
                
                config_data['CANCELLATION_WINDOW_HOURS'] = horas
                current_app.config['CANCELLATION_WINDOW_HOURS'] = horas
                
                flash(f'Janela de cancelamento atualizada para {horas} horas!', 'success')
                
            elif form_type == 'valores':
                # Valores sugeridos por categoria
                valores = {
                    'garcom': float(request.form.get('valor_garcom', 15)),
                    'bartender': float(request.form.get('valor_bartender', 20)),
                    'organizacao': float(request.form.get('valor_organizacao', 18))
                }
                
                config_data['VALORES_SUGERIDOS'] = valores
                current_app.config['VALORES_SUGERIDOS'] = valores
                
                flash('Valores sugeridos atualizados!', 'success')
                
            elif form_type == 'termos':
                # Termos e políticas
                config_data['TERMOS_DE_USO'] = request.form.get('termos_uso', '').strip()
                config_data['POLITICA_PRIVACIDADE'] = request.form.get('politica_privacidade', '').strip()
                config_data['POLITICA_CANCELAMENTO'] = request.form.get('politica_cancelamento', '').strip()
                
                current_app.config['TERMOS_DE_USO'] = config_data['TERMOS_DE_USO']
                current_app.config['POLITICA_PRIVACIDADE'] = config_data['POLITICA_PRIVACIDADE']
                current_app.config['POLITICA_CANCELAMENTO'] = config_data['POLITICA_CANCELAMENTO']
                
                flash('Termos e políticas atualizados!', 'success')
            
            save_platform_config(config_data)
            
        except ValueError as e:
            flash(f'Valor inválido: {str(e)}', 'danger')
        
        return redirect(url_for('admin.configuracoes'))
    
    # GET: mostrar formulário com valores atuais
    config_atual = {
        'platform_name': current_app.config.get('PLATFORM_NAME', 'ExtraSITE'),
        'platform_city': current_app.config.get('PLATFORM_CITY', 'Medianeira - PR'),
        'taxa_atual': current_app.config.get('TAKE_RATE', 0.15) * 100,
        'cancellation_hours': current_app.config.get('CANCELLATION_WINDOW_HOURS', 48),
        'valores_sugeridos': current_app.config.get('VALORES_SUGERIDOS', {
            'garcom': 15.0,
            'bartender': 20.0,
            'organizacao': 18.0
        }),
        'termos_uso': current_app.config.get('TERMOS_DE_USO', ''),
        'politica_privacidade': current_app.config.get('POLITICA_PRIVACIDADE', ''),
        'politica_cancelamento': current_app.config.get('POLITICA_CANCELAMENTO', ''),
    }
    
    return render_template('admin/configuracoes.html', config=config_atual)
