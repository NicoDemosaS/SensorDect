# Rotas de configuracao
from flask import Blueprint, render_template, jsonify, redirect, request, session, url_for
config_bp = Blueprint('config', __name__)


@config_bp.route("/config")
def config():
    #Rota para configuração do alarme
    return render_template("config.html")

# Rota para ativar/desativar o alarme

@config_bp.route("/ativar-alarme", methods = ['POST', 'GET'])
def ativar_alarme():
    # Lógica para ativar o alarme
    alarm_status = True
    return jsonify({"status": "Alarme ativado", "alarm_status": alarm_status})

@config_bp.route("/desativar-alarme", methods = ['POST', 'GET'])
def desativar_alarme():
    # Lógica para desativar o alarme
    alarm_status = False
    return jsonify({"status": "Alarme desativado", "alarm_status": alarm_status})

@config_bp.route("/status-alarme", methods = ['GET'])
def status_alarme():
    # Lógica para verificar o status do alarme
    alarm_status = False  # Exemplo de status
    return jsonify({"alarm_status": alarm_status})
