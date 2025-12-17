from flask import Blueprint, render_template, jsonify, redirect, request, session, url_for
from utils import login_required
alarm_bp = Blueprint('alarm', __name__)

# Rotas do Alarme, ativar desativar e status


@alarm_bp.route("/ativar-alarme", methods = ['POST', 'GET'])
@login_required
def ativar_alarme():
    # Lógica para ativar o alarme
    alarm_status = True
    return jsonify({"status": "Alarme ativado", "alarm_status": alarm_status})

@alarm_bp.route("/desativar-alarme", methods = ['POST', 'GET'])
@login_required
def desativar_alarme():
    # Lógica para desativar o alarme
    alarm_status = False
    return jsonify({"status": "Alarme desativado", "alarm_status": alarm_status})

@alarm_bp.route("/status-alarme", methods = ['GET'])
@login_required
def status_alarme():
    # Lógica para verificar o status do alarme
    alarm_status = False  # Exemplo de status
    return jsonify({"alarm_status": alarm_status})
