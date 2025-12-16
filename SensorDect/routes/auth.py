# Rotas de autenticacao
from flask import Blueprint, render_template, redirect, request, session, url_for

auth_bp = Blueprint('auth', __name__)


@auth_bp.route("/")
def home():    
    #Rota para a página inicial (login)
    # Se estiver logado -> redirect para o dashboard
    return redirect(url_for("auth.login"))
    # Se estiver deslogado -> redirect para o login

@auth_bp.route("/login", methods = ['POST', 'GET'])
def login():
    #Rota para o login do usuário
    if request.method == 'POST':
        # Captura os dados enviados pelo formulário
        username = request.form.get("username")
        password = request.form.get("password")
        
        # Aqui você pode adicionar lógica de validação
        print(f"Login tentado - Username: {username}, Password: {password}")
        if username == "Maquiavel" and password == "haha!":
            session['logged_in'] = True
            session['username'] = username
            return redirect("/dashboard")
        else:
            return render_template("index.html", error="Credenciais inválidas")
    
    # Se for GET, apenas mostra a página de login
    return render_template("index.html")

