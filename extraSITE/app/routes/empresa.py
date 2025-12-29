from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from functools import wraps
from datetime import datetime

from app import db
from app.models import Trabalho, Candidatura
from app.forms.empresa import TrabalhoForm, EditarEmpresaForm
from app.utils.email import email_candidatura_aceita, email_candidatura_recusada, email_trabalho_confirmado

empresa_bp = Blueprint('empresa', __name__)


def empresa_required(f):
    """Decorator que exige que o usuário seja uma empresa."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.tipo_usuario != 'empresa':
            flash('Acesso restrito a empresas.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


def empresa_ativa_required(f):
    """Decorator que exige empresa ativa (aprovada)."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.pode_publicar:
            flash('Sua empresa ainda não foi aprovada. Aguarde a validação.', 'warning')
            return redirect(url_for('empresa.dashboard'))
        return f(*args, **kwargs)
    return decorated_function


@empresa_bp.route('/dashboard')
@login_required
@empresa_required
def dashboard():
    """Dashboard da empresa."""
    trabalhos = Trabalho.query.filter_by(empresa_id=current_user.id).order_by(
        Trabalho.data.desc()
    ).limit(10).all()
    
    # Contadores
    trabalhos_abertos = Trabalho.query.filter_by(
        empresa_id=current_user.id, status='aberto'
    ).count()
    
    trabalhos_concluidos = Trabalho.query.filter_by(
        empresa_id=current_user.id, status='concluido'
    ).count()
    
    return render_template('empresa/dashboard.html',
                         trabalhos=trabalhos,
                         trabalhos_abertos=trabalhos_abertos,
                         trabalhos_concluidos=trabalhos_concluidos)


@empresa_bp.route('/trabalho/novo', methods=['GET', 'POST'])
@login_required
@empresa_required
@empresa_ativa_required
def novo_trabalho():
    """Criar novo trabalho."""
    form = TrabalhoForm()
    
    if form.validate_on_submit():
        trabalho = Trabalho(
            empresa_id=current_user.id,
            titulo=form.titulo.data,
            descricao=form.descricao.data,
            categoria=form.categoria.data,
            requisitos=form.requisitos.data,
            local_endereco=form.local_endereco.data,
            local_cidade=form.local_cidade.data,
            data=form.data.data,
            horario_inicio=form.horario_inicio.data,
            horario_fim=form.horario_fim.data,
            valor_pagamento=form.valor_pagamento.data,
            vagas_total=form.vagas_total.data,
            status='aberto'
        )
        
        # Calcula valor sugerido
        trabalho.calcular_valor_sugerido()
        
        db.session.add(trabalho)
        db.session.commit()
        
        flash('Trabalho publicado com sucesso!', 'success')
        return redirect(url_for('empresa.ver_trabalho', trabalho_id=trabalho.id))
    
    return render_template('empresa/novo_trabalho.html', form=form, categorias=Trabalho.CATEGORIAS)


@empresa_bp.route('/trabalho/<trabalho_id>')
@login_required
@empresa_required
def ver_trabalho(trabalho_id):
    """Visualiza detalhes de um trabalho e suas candidaturas."""
    trabalho = Trabalho.query.get_or_404(trabalho_id)
    
    if trabalho.empresa_id != current_user.id:
        flash('Você não tem permissão para ver este trabalho.', 'danger')
        return redirect(url_for('empresa.dashboard'))
    
    candidaturas = Candidatura.query.filter_by(trabalho_id=trabalho_id).all()
    
    return render_template('empresa/trabalho.html',
                         trabalho=trabalho,
                         candidaturas=candidaturas)


@empresa_bp.route('/trabalho/<trabalho_id>/candidatura/<candidatura_id>/aceitar', methods=['POST'])
@login_required
@empresa_required
def aceitar_candidatura(trabalho_id, candidatura_id):
    """Aceita uma candidatura."""
    trabalho = Trabalho.query.get_or_404(trabalho_id)
    candidatura = Candidatura.query.get_or_404(candidatura_id)
    
    if trabalho.empresa_id != current_user.id:
        flash('Você não tem permissão para esta ação.', 'danger')
        return redirect(url_for('empresa.dashboard'))
    
    if trabalho.vagas_disponiveis <= 0:
        flash('Todas as vagas já foram preenchidas.', 'warning')
        return redirect(url_for('empresa.ver_trabalho', trabalho_id=trabalho_id))
    
    candidatura.aceitar()
    db.session.commit()
    
    # Envia email notificando o colaborador
    email_candidatura_aceita(
        nome=candidatura.colaborador.nome,
        email=candidatura.colaborador.email,
        trabalho_titulo=trabalho.titulo,
        empresa_nome=current_user.nome_fantasia,
        data=trabalho.data.strftime('%d/%m/%Y'),
        horario=f"{trabalho.horario_inicio.strftime('%H:%M')} - {trabalho.horario_fim.strftime('%H:%M')}",
        local=f"{trabalho.local_endereco}, {trabalho.local_cidade}",
        valor=trabalho.valor_liquido
    )
    
    flash(f'Candidatura de {candidatura.colaborador.nome} aceita!', 'success')
    return redirect(url_for('empresa.ver_trabalho', trabalho_id=trabalho_id))


@empresa_bp.route('/trabalho/<trabalho_id>/candidatura/<candidatura_id>/recusar', methods=['POST'])
@login_required
@empresa_required
def recusar_candidatura(trabalho_id, candidatura_id):
    """Recusa uma candidatura."""
    trabalho = Trabalho.query.get_or_404(trabalho_id)
    candidatura = Candidatura.query.get_or_404(candidatura_id)
    
    if trabalho.empresa_id != current_user.id:
        flash('Você não tem permissão para esta ação.', 'danger')
        return redirect(url_for('empresa.dashboard'))
    
    candidatura.recusar()
    db.session.commit()
    
    # Envia email notificando o colaborador
    email_candidatura_recusada(
        nome=candidatura.colaborador.nome,
        email=candidatura.colaborador.email,
        trabalho_titulo=trabalho.titulo
    )
    
    flash('Candidatura recusada.', 'info')
    return redirect(url_for('empresa.ver_trabalho', trabalho_id=trabalho_id))


@empresa_bp.route('/trabalho/<trabalho_id>/confirmar/<candidatura_id>', methods=['POST'])
@login_required
@empresa_required
def confirmar_execucao(trabalho_id, candidatura_id):
    """Confirma que o colaborador executou o trabalho."""
    trabalho = Trabalho.query.get_or_404(trabalho_id)
    candidatura = Candidatura.query.get_or_404(candidatura_id)
    
    if trabalho.empresa_id != current_user.id:
        flash('Você não tem permissão para esta ação.', 'danger')
        return redirect(url_for('empresa.dashboard'))
    
    candidatura.confirmado_empresa = True
    candidatura.compareceu = True
    db.session.commit()
    
    # Envia email notificando o colaborador do pagamento
    email_trabalho_confirmado(
        nome=candidatura.colaborador.nome,
        email=candidatura.colaborador.email,
        trabalho_titulo=trabalho.titulo,
        valor=trabalho.valor_liquido
    )
    
    flash(f'Execução de {candidatura.colaborador.nome} confirmada!', 'success')
    return redirect(url_for('empresa.ver_trabalho', trabalho_id=trabalho_id))


@empresa_bp.route('/trabalho/<trabalho_id>/nao-compareceu/<candidatura_id>', methods=['POST'])
@login_required
@empresa_required
def marcar_nao_compareceu(trabalho_id, candidatura_id):
    """Marca que o colaborador não compareceu."""
    trabalho = Trabalho.query.get_or_404(trabalho_id)
    candidatura = Candidatura.query.get_or_404(candidatura_id)
    
    if trabalho.empresa_id != current_user.id:
        flash('Você não tem permissão para esta ação.', 'danger')
        return redirect(url_for('empresa.dashboard'))
    
    candidatura.confirmado_empresa = True
    candidatura.compareceu = False
    db.session.commit()
    
    flash(f'{candidatura.colaborador.nome} foi marcado como não compareceu.', 'warning')
    return redirect(url_for('empresa.ver_trabalho', trabalho_id=trabalho_id))


@empresa_bp.route('/trabalho/<trabalho_id>/concluir', methods=['POST'])
@login_required
@empresa_required
def concluir_trabalho(trabalho_id):
    """Marca o trabalho como concluído."""
    trabalho = Trabalho.query.get_or_404(trabalho_id)
    
    if trabalho.empresa_id != current_user.id:
        flash('Você não tem permissão para esta ação.', 'danger')
        return redirect(url_for('empresa.dashboard'))
    
    trabalho.status = 'concluido'
    db.session.commit()
    
    flash('Trabalho marcado como concluído!', 'success')
    return redirect(url_for('empresa.dashboard'))


@empresa_bp.route('/meus-trabalhos')
@login_required
@empresa_required
def meus_trabalhos():
    """Lista todos os trabalhos da empresa."""
    trabalhos = Trabalho.query.filter_by(empresa_id=current_user.id).order_by(
        Trabalho.criado_em.desc()
    ).all()
    
    return render_template('empresa/meus_trabalhos.html', trabalhos=trabalhos)


@empresa_bp.route('/perfil', methods=['GET', 'POST'])
@login_required
@empresa_required
def perfil():
    """Editar perfil da empresa."""
    form = EditarEmpresaForm(obj=current_user)
    
    if form.validate_on_submit():
        current_user.nome_fantasia = form.nome_fantasia.data
        current_user.telefone = form.telefone.data
        current_user.pessoa_contato = form.pessoa_contato.data
        current_user.endereco_rua = form.endereco_rua.data
        current_user.endereco_cidade = form.endereco_cidade.data
        current_user.endereco_estado = form.endereco_estado.data
        current_user.endereco_cep = form.endereco_cep.data
        
        db.session.commit()
        flash('Perfil atualizado com sucesso!', 'success')
        return redirect(url_for('empresa.perfil'))
    
    return render_template('empresa/perfil.html', form=form)
