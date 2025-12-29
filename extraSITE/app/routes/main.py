from flask import Blueprint, render_template, current_app
from flask_login import current_user

from app.models import Trabalho

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Página inicial."""
    # Busca trabalhos abertos para exibir na home
    trabalhos_recentes = Trabalho.query.filter_by(status='aberto').order_by(
        Trabalho.data.asc()
    ).limit(6).all()
    
    return render_template('main/index.html', trabalhos=trabalhos_recentes)


@main_bp.route('/sobre')
def sobre():
    """Página sobre a plataforma."""
    return render_template('main/sobre.html')


@main_bp.route('/termos')
def termos():
    """Página de termos de uso."""
    return render_template('main/termos.html')


@main_bp.route('/privacidade')
def privacidade():
    """Página de política de privacidade."""
    return render_template('main/privacidade.html')


@main_bp.route('/cancelamento')
def cancelamento():
    """Página de política de cancelamento."""
    return render_template('main/cancelamento.html')
