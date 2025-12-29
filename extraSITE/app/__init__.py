import os
import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

from config import config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()

login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'
login_manager.login_message_category = 'warning'


def load_platform_config(app):
    """Carrega configurações personalizadas da plataforma."""
    config_path = os.path.join(app.instance_path, 'platform_config.json')
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            custom_config = json.load(f)
            for key, value in custom_config.items():
                app.config[key] = value


def create_app(config_name='default'):
    """Factory de criação da aplicação Flask."""
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Inicializa extensões
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    
    # Inicializa sistema de emails (Resend)
    from app.utils.email import init_resend
    init_resend(app)
    
    # Cria pasta de uploads se não existir
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(app.instance_path), exist_ok=True)
    
    # Carrega configurações personalizadas (ex: taxa da plataforma)
    load_platform_config(app)
    
    # Registra blueprints
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.colaborador import colaborador_bp
    from app.routes.empresa import empresa_bp
    from app.routes.admin import admin_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(colaborador_bp, url_prefix='/colaborador')
    app.register_blueprint(empresa_bp, url_prefix='/empresa')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    # Context processor para variáveis globais nos templates
    @app.context_processor
    def inject_platform_config():
        """Injeta configurações da plataforma em todos os templates."""
        return {
            'PLATFORM_NAME': app.config.get('PLATFORM_NAME', 'ExtraSITE'),
            'PLATFORM_CITY': app.config.get('PLATFORM_CITY', 'Medianeira - PR'),
            'TAKE_RATE': app.config.get('TAKE_RATE', 0.15),
            'TAKE_RATE_PERCENT': int(app.config.get('TAKE_RATE', 0.15) * 100),
            'CANCELLATION_WINDOW_HOURS': app.config.get('CANCELLATION_WINDOW_HOURS', 48),
            'VALORES_SUGERIDOS': app.config.get('VALORES_SUGERIDOS', {
                'garcom': 15.0,
                'bartender': 20.0,
                'organizacao': 18.0
            }),
            'TERMOS_DE_USO': app.config.get('TERMOS_DE_USO', ''),
            'POLITICA_PRIVACIDADE': app.config.get('POLITICA_PRIVACIDADE', ''),
            'POLITICA_CANCELAMENTO': app.config.get('POLITICA_CANCELAMENTO', ''),
        }
    
    # Criar tabelas do banco
    with app.app_context():
        db.create_all()
    
    return app
