import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Configurações base da aplicação."""
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # SQLite para desenvolvimento, PostgreSQL para produção
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'extrasite.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload de arquivos
    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    # Configurações da plataforma
    PLATFORM_NAME = 'ExtraSITE'
    PLATFORM_CITY = 'Medianeira - PR'
    TAKE_RATE = 0.15  # 15% de taxa da plataforma
    CANCELLATION_WINDOW_HOURS = 48  # Janela de cancelamento sem penalidade
    
    # Configurações de Email (Resend)
    RESEND_API_KEY = os.environ.get('RESEND_API_KEY') or 're_2Ry9wHL6_6HoWggikBbVD9A2rvvWcDBdn'
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'ExtraSITE <onboarding@resend.dev>'
    
    # Valores sugeridos por categoria (por hora)
    VALORES_SUGERIDOS = {
        'garcom': 15.0,
        'bartender': 20.0,
        'organizacao': 18.0
    }
    
    # Termos e políticas
    TERMOS_DE_USO = ''
    POLITICA_PRIVACIDADE = ''
    POLITICA_CANCELAMENTO = ''


class DevelopmentConfig(Config):
    """Configurações de desenvolvimento."""
    DEBUG = True


class ProductionConfig(Config):
    """Configurações de produção."""
    DEBUG = False
    # Em produção, usar variáveis de ambiente para SECRET_KEY e DATABASE_URL


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
