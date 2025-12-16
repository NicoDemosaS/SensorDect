# Rotas do dashboard
from flask import Blueprint, render_template, redirect, request, session, url_for
dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route("/dashboard")
def dashboard():
    #Rota para o dashboard do sistema de alarme
    return render_template("dashboard.html")