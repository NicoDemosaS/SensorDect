"""
Script para criar o primeiro administrador do sistema.
Execute com: python create_admin.py
"""

from app import create_app, db
from app.models import Admin

app = create_app()

with app.app_context():
    # Verifica se já existe admin
    if Admin.query.first():
        print("Já existe um administrador cadastrado!")
        print("Admins existentes:")
        for admin in Admin.query.all():
            print(f"  - {admin.email}")
    else:
        # Cria admin padrão
        email = input("Email do admin: ") or "admin@extrasite.com"
        nome = input("Nome do admin: ") or "Administrador"
        senha = input("Senha: ") or "admin123"
        
        admin = Admin(
            nome=nome,
            email=email
        )
        admin.set_senha(senha)
        
        db.session.add(admin)
        db.session.commit()
        
        print(f"\n✅ Admin criado com sucesso!")
        print(f"   Email: {email}")
        print(f"   Acesse: /admin/login")
