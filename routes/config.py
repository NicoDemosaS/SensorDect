# Rotas de configuracao
from flask import Blueprint, render_template, jsonify, redirect, request, session, url_for
from utils import login_required
config_bp = Blueprint('config', __name__)


@config_bp.route("/config")
@login_required
def config():
    #Rota para configuração do alarme
    return render_template("config.html")


