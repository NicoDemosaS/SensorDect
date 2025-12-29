from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from functools import wraps

from app import db
from app.models import Trabalho, Candidatura
from app.forms.colaborador import EditarPerfilForm, CandidaturaForm
from app.utils.email import email_candidatura_enviada, email_nova_candidatura

colaborador_bp = Blueprint('colaborador', __name__)


def colaborador_required(f):
    """Decorator que exige que o usuário seja um colaborador."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.tipo_usuario != 'colaborador':
            flash('Acesso restrito a colaboradores.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


@colaborador_bp.route('/dashboard')
@login_required
@colaborador_required
def dashboard():
    """Dashboard do colaborador."""
    # Candidaturas aceitas (trabalhos confirmados)
    candidaturas_aceitas = Candidatura.query.filter_by(
        colaborador_id=current_user.id,
        status='aceita'
    ).join(Trabalho).order_by(Trabalho.data.asc()).all()
    
    # Candidaturas pendentes
    candidaturas_pendentes = Candidatura.query.filter_by(
        colaborador_id=current_user.id,
        status='pendente'
    ).all()
    
    return render_template('colaborador/dashboard.html',
                         aceitas=candidaturas_aceitas,
                         pendentes=candidaturas_pendentes)


@colaborador_bp.route('/mural')
@login_required
@colaborador_required
def mural():
    """Mural de trabalhos disponíveis."""
    # Filtros
    categoria = request.args.get('categoria', '')
    cidade = request.args.get('cidade', '')
    
    # Query base
    query = Trabalho.query.filter_by(status='aberto')
    
    # Aplica filtros
    if categoria:
        query = query.filter_by(categoria=categoria)
    if cidade:
        query = query.filter(Trabalho.local_cidade.ilike(f'%{cidade}%'))
    
    # Ordena por data
    trabalhos = query.order_by(Trabalho.data.asc()).all()
    
    # IDs de trabalhos que o colaborador já se candidatou
    candidaturas_ids = [c.trabalho_id for c in current_user.candidaturas]
    
    return render_template('colaborador/mural.html',
                         trabalhos=trabalhos,
                         candidaturas_ids=candidaturas_ids,
                         categorias=Trabalho.CATEGORIAS,
                         filtro_categoria=categoria,
                         filtro_cidade=cidade)


@colaborador_bp.route('/trabalho/<trabalho_id>')
@login_required
@colaborador_required
def ver_trabalho(trabalho_id):
    """Visualiza detalhes de um trabalho."""
    trabalho = Trabalho.query.get_or_404(trabalho_id)
    
    # Verifica se já se candidatou
    candidatura_existente = Candidatura.query.filter_by(
        trabalho_id=trabalho_id,
        colaborador_id=current_user.id
    ).first()
    
    form = CandidaturaForm()
    
    return render_template('colaborador/trabalho.html',
                         trabalho=trabalho,
                         candidatura=candidatura_existente,
                         form=form)


@colaborador_bp.route('/trabalho/<trabalho_id>/candidatar', methods=['POST'])
@login_required
@colaborador_required
def candidatar(trabalho_id):
    """Candidata-se a um trabalho."""
    trabalho = Trabalho.query.get_or_404(trabalho_id)
    
    if not trabalho.esta_aberto:
        flash('Este trabalho não está mais aceitando candidaturas.', 'warning')
        return redirect(url_for('colaborador.ver_trabalho', trabalho_id=trabalho_id))
    
    # Verifica se já se candidatou
    existente = Candidatura.query.filter_by(
        trabalho_id=trabalho_id,
        colaborador_id=current_user.id
    ).first()
    
    if existente:
        flash('Você já se candidatou a este trabalho.', 'info')
        return redirect(url_for('colaborador.ver_trabalho', trabalho_id=trabalho_id))
    
    form = CandidaturaForm()
    
    if form.validate_on_submit():
        candidatura = Candidatura(
            trabalho_id=trabalho_id,
            colaborador_id=current_user.id,
            mensagem=form.mensagem.data
        )
        
        db.session.add(candidatura)
        db.session.commit()
        
        # Envia email para o colaborador confirmando candidatura
        email_candidatura_enviada(
            nome=current_user.nome,
            email=current_user.email,
            trabalho_titulo=trabalho.titulo,
            empresa_nome=trabalho.empresa.nome_fantasia,
            data=trabalho.data.strftime('%d/%m/%Y'),
            valor=trabalho.valor_liquido
        )
        
        # Notifica a empresa sobre nova candidatura
        email_nova_candidatura(
            empresa_email=trabalho.empresa.email,
            empresa_nome=trabalho.empresa.nome_fantasia,
            colaborador_nome=current_user.nome,
            trabalho_titulo=trabalho.titulo
        )
        
        flash('Candidatura enviada com sucesso!', 'success')
    
    return redirect(url_for('colaborador.ver_trabalho', trabalho_id=trabalho_id))


@colaborador_bp.route('/candidatura/<candidatura_id>/cancelar', methods=['POST'])
@login_required
@colaborador_required
def cancelar_candidatura(candidatura_id):
    """Cancela uma candidatura."""
    candidatura = Candidatura.query.get_or_404(candidatura_id)
    
    if candidatura.colaborador_id != current_user.id:
        flash('Você não tem permissão para cancelar esta candidatura.', 'danger')
        return redirect(url_for('colaborador.dashboard'))
    
    candidatura.cancelar()
    db.session.commit()
    
    flash('Candidatura cancelada.', 'info')
    return redirect(url_for('colaborador.dashboard'))


@colaborador_bp.route('/minhas-candidaturas')
@login_required
@colaborador_required
def minhas_candidaturas():
    """Lista todas as candidaturas do colaborador."""
    candidaturas = Candidatura.query.filter_by(
        colaborador_id=current_user.id
    ).order_by(Candidatura.candidatou_em.desc()).all()
    
    return render_template('colaborador/candidaturas.html', candidaturas=candidaturas)


@colaborador_bp.route('/perfil', methods=['GET', 'POST'])
@login_required
@colaborador_required
def perfil():
    """Editar perfil do colaborador."""
    form = EditarPerfilForm(obj=current_user)
    
    if form.validate_on_submit():
        current_user.nome = form.nome.data
        current_user.telefone = form.telefone.data
        current_user.universidade = form.universidade.data
        current_user.bio = form.bio.data
        current_user.habilidades = form.habilidades.data
        current_user.chave_pix = form.chave_pix.data
        
        db.session.commit()
        flash('Perfil atualizado com sucesso!', 'success')
        return redirect(url_for('colaborador.perfil'))
    
    return render_template('colaborador/perfil.html', form=form)
