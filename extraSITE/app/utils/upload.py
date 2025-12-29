import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app


def allowed_file(filename):
    """Verifica se a extensão do arquivo é permitida."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def salvar_imagem(file, pasta='geral'):
    """
    Salva uma imagem no servidor.
    
    Args:
        file: FileStorage object do Flask
        pasta: Subpasta dentro de uploads (perfil, empresas, etc)
    
    Returns:
        Nome do arquivo salvo ou None se falhar
    """
    if file and allowed_file(file.filename):
        # Gera nome único
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"
        
        # Cria pasta se não existir
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], pasta)
        os.makedirs(upload_path, exist_ok=True)
        
        # Salva arquivo
        file_path = os.path.join(upload_path, filename)
        file.save(file_path)
        
        # Retorna caminho relativo para salvar no banco
        return f"{pasta}/{filename}"
    
    return None


def deletar_imagem(filepath):
    """Deleta uma imagem do servidor."""
    if filepath:
        full_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filepath)
        if os.path.exists(full_path):
            os.remove(full_path)
            return True
    return False
