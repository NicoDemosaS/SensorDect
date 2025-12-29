from app import create_app, db
from app.models import Colaborador, Empresa, Trabalho, Candidatura, Admin

app = create_app()


@app.shell_context_processor
def make_shell_context():
    """Contexto para o flask shell."""
    return {
        'db': db,
        'Colaborador': Colaborador,
        'Empresa': Empresa,
        'Trabalho': Trabalho,
        'Candidatura': Candidatura,
        'Admin': Admin
    }


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
