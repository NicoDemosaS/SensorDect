from flask import Flask
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.config import config_bp
from routes.alarm import alarm_bp
app = Flask(__name__)

app.secret_key = 'chave_secreta'  # Necessário para usar sessões

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(config_bp)
app.register_blueprint(alarm_bp)

if __name__ == "__main__":

    app.run(debug=True)