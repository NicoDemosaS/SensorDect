"""
Sistema de envio de emails usando Resend.
"""
import resend
from flask import current_app, render_template_string
from threading import Thread


def init_resend(app):
    """Inicializa o Resend com a API key."""
    resend.api_key = app.config.get('RESEND_API_KEY')


def enviar_email_async(app, destinatario, assunto, html):
    """Envia email de forma assíncrona."""
    with app.app_context():
        try:
            params = {
                "from": current_app.config.get('MAIL_DEFAULT_SENDER', 'ExtraSITE <onboarding@resend.dev>'),
                "to": [destinatario],
                "subject": assunto,
                "html": html
            }
            resend.Emails.send(params)
        except Exception as e:
            print(f"Erro ao enviar email: {e}")


def enviar_email(destinatario, assunto, html):
    """
    Envia um email usando Resend.
    
    Args:
        destinatario: Email do destinatário
        assunto: Assunto do email
        html: Corpo do email em HTML
    """
    app = current_app._get_current_object()
    
    # Envia em thread separada para não bloquear
    thread = Thread(target=enviar_email_async, args=(app, destinatario, assunto, html))
    thread.start()


# ============================================
# TEMPLATES DE EMAIL
# ============================================

def get_email_base(conteudo, titulo=""):
    """Template base para todos os emails."""
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f8fafc;">
        <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f8fafc; padding: 40px 20px;">
            <tr>
                <td align="center">
                    <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 16px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                        <!-- Header -->
                        <tr>
                            <td style="background: linear-gradient(135deg, #7c3aed 0%, #06b6d4 100%); padding: 32px; text-align: center; border-radius: 16px 16px 0 0;">
                                <h1 style="color: #ffffff; margin: 0; font-size: 28px; font-weight: 800;">ExtraSITE</h1>
                                <p style="color: rgba(255,255,255,0.9); margin: 8px 0 0; font-size: 14px;">Freelance Universitário</p>
                            </td>
                        </tr>
                        
                        <!-- Content -->
                        <tr>
                            <td style="padding: 40px 32px;">
                                {conteudo}
                            </td>
                        </tr>
                        
                        <!-- Footer -->
                        <tr>
                            <td style="background-color: #f1f5f9; padding: 24px 32px; text-align: center; border-radius: 0 0 16px 16px;">
                                <p style="color: #64748b; font-size: 12px; margin: 0;">
                                    Este email foi enviado automaticamente pela plataforma ExtraSITE.<br>
                                    Medianeira - PR | © 2025
                                </p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    '''


# ============================================
# EMAILS PARA COLABORADORES
# ============================================

def email_boas_vindas_colaborador(nome, email):
    """Email de boas-vindas para novo colaborador."""
    conteudo = f'''
        <h2 style="color: #1e293b; margin: 0 0 16px;">Bem-vindo(a), {nome}! 🎉</h2>
        <p style="color: #475569; font-size: 16px; line-height: 1.6; margin: 0 0 24px;">
            Sua conta foi criada com sucesso! Agora você faz parte da maior comunidade de universitários freelancers da região.
        </p>
        
        <div style="background: linear-gradient(135deg, rgba(124, 58, 237, 0.1), rgba(6, 182, 212, 0.1)); border-radius: 12px; padding: 24px; margin: 24px 0;">
            <h3 style="color: #7c3aed; margin: 0 0 16px; font-size: 18px;">📋 Próximos passos:</h3>
            <ol style="color: #475569; padding-left: 20px; margin: 0;">
                <li style="margin-bottom: 12px;">Complete seu perfil com foto e habilidades</li>
                <li style="margin-bottom: 12px;">Navegue pelo mural de oportunidades</li>
                <li style="margin-bottom: 12px;">Candidate-se aos trabalhos que combinam com você</li>
                <li>Receba o pagamento após cada trabalho concluído!</li>
            </ol>
        </div>
        
        <p style="color: #475569; font-size: 16px; line-height: 1.6;">
            💰 <strong>Pagamento garantido</strong> pela plataforma após confirmação do trabalho.
        </p>
        
        <div style="text-align: center; margin: 32px 0;">
            <a href="https://extrasite.com/colaborador/mural" style="display: inline-block; background: linear-gradient(135deg, #7c3aed, #06b6d4); color: #ffffff; text-decoration: none; padding: 16px 32px; border-radius: 12px; font-weight: 600; font-size: 16px;">
                Ver Oportunidades
            </a>
        </div>
    '''
    
    enviar_email(email, "🎓 Bem-vindo(a) ao ExtraSITE!", get_email_base(conteudo))


def email_candidatura_enviada(nome, email, trabalho_titulo, empresa_nome, data, valor):
    """Email confirmando envio de candidatura."""
    conteudo = f'''
        <h2 style="color: #1e293b; margin: 0 0 16px;">Candidatura Enviada! ✅</h2>
        <p style="color: #475569; font-size: 16px; line-height: 1.6; margin: 0 0 24px;">
            Olá {nome}, sua candidatura foi enviada com sucesso!
        </p>
        
        <div style="background-color: #f8fafc; border-radius: 12px; padding: 24px; border-left: 4px solid #7c3aed;">
            <h3 style="color: #1e293b; margin: 0 0 16px;">{trabalho_titulo}</h3>
            <p style="color: #64748b; margin: 0 0 8px;">🏢 <strong>{empresa_nome}</strong></p>
            <p style="color: #64748b; margin: 0 0 8px;">📅 {data}</p>
            <p style="color: #10b981; margin: 0; font-size: 20px; font-weight: 700;">💰 R$ {valor:.2f}</p>
        </div>
        
        <p style="color: #475569; font-size: 16px; line-height: 1.6; margin: 24px 0;">
            A empresa analisará seu perfil e você receberá uma notificação assim que houver uma resposta.
        </p>
        
        <p style="color: #94a3b8; font-size: 14px;">
            ⏳ Tempo médio de resposta: 24-48 horas
        </p>
    '''
    
    enviar_email(email, f"✅ Candidatura enviada: {trabalho_titulo}", get_email_base(conteudo))


def email_candidatura_aceita(nome, email, trabalho_titulo, empresa_nome, data, horario, local, valor):
    """Email notificando que candidatura foi aceita."""
    conteudo = f'''
        <h2 style="color: #10b981; margin: 0 0 16px;">Parabéns! Você foi selecionado! 🎉</h2>
        <p style="color: #475569; font-size: 16px; line-height: 1.6; margin: 0 0 24px;">
            Olá {nome}, a empresa <strong>{empresa_nome}</strong> aceitou sua candidatura!
        </p>
        
        <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(6, 182, 212, 0.1)); border-radius: 12px; padding: 24px; border: 2px solid #10b981;">
            <h3 style="color: #1e293b; margin: 0 0 16px;">📋 Detalhes do Trabalho</h3>
            <table style="width: 100%; color: #475569;">
                <tr><td style="padding: 8px 0;"><strong>Trabalho:</strong></td><td>{trabalho_titulo}</td></tr>
                <tr><td style="padding: 8px 0;"><strong>Empresa:</strong></td><td>{empresa_nome}</td></tr>
                <tr><td style="padding: 8px 0;"><strong>Data:</strong></td><td>{data}</td></tr>
                <tr><td style="padding: 8px 0;"><strong>Horário:</strong></td><td>{horario}</td></tr>
                <tr><td style="padding: 8px 0;"><strong>Local:</strong></td><td>{local}</td></tr>
                <tr><td style="padding: 8px 0;"><strong>Valor:</strong></td><td style="color: #10b981; font-weight: 700; font-size: 18px;">R$ {valor:.2f}</td></tr>
            </table>
        </div>
        
        <div style="background-color: #fef3c7; border-radius: 12px; padding: 16px; margin: 24px 0;">
            <p style="color: #92400e; margin: 0; font-size: 14px;">
                ⚠️ <strong>Importante:</strong> Compareça no horário combinado. Faltas sem aviso prévio podem resultar em penalidades.
            </p>
        </div>
        
        <div style="text-align: center; margin: 32px 0;">
            <a href="https://extrasite.com/colaborador/dashboard" style="display: inline-block; background: #10b981; color: #ffffff; text-decoration: none; padding: 16px 32px; border-radius: 12px; font-weight: 600; font-size: 16px;">
                Ver Meus Trabalhos
            </a>
        </div>
    '''
    
    enviar_email(email, f"🎉 Você foi selecionado: {trabalho_titulo}", get_email_base(conteudo))


def email_candidatura_recusada(nome, email, trabalho_titulo):
    """Email notificando que candidatura foi recusada."""
    conteudo = f'''
        <h2 style="color: #1e293b; margin: 0 0 16px;">Atualização da sua candidatura</h2>
        <p style="color: #475569; font-size: 16px; line-height: 1.6; margin: 0 0 24px;">
            Olá {nome}, infelizmente sua candidatura para <strong>{trabalho_titulo}</strong> não foi selecionada desta vez.
        </p>
        
        <p style="color: #475569; font-size: 16px; line-height: 1.6;">
            Não desanime! Novas oportunidades surgem todos os dias. Continue se candidatando! 💪
        </p>
        
        <div style="text-align: center; margin: 32px 0;">
            <a href="https://extrasite.com/colaborador/mural" style="display: inline-block; background: linear-gradient(135deg, #7c3aed, #06b6d4); color: #ffffff; text-decoration: none; padding: 16px 32px; border-radius: 12px; font-weight: 600; font-size: 16px;">
                Ver Novas Oportunidades
            </a>
        </div>
    '''
    
    enviar_email(email, f"Atualização: {trabalho_titulo}", get_email_base(conteudo))


def email_trabalho_confirmado(nome, email, trabalho_titulo, valor):
    """Email notificando que trabalho foi confirmado pela empresa."""
    conteudo = f'''
        <h2 style="color: #10b981; margin: 0 0 16px;">Trabalho Confirmado! 💰</h2>
        <p style="color: #475569; font-size: 16px; line-height: 1.6; margin: 0 0 24px;">
            Olá {nome}, a empresa confirmou sua presença no trabalho <strong>{trabalho_titulo}</strong>!
        </p>
        
        <div style="background: linear-gradient(135deg, #10b981, #06b6d4); border-radius: 12px; padding: 32px; text-align: center; color: #ffffff;">
            <p style="margin: 0 0 8px; font-size: 14px; opacity: 0.9;">Valor a receber:</p>
            <p style="margin: 0; font-size: 36px; font-weight: 800;">R$ {valor:.2f}</p>
        </div>
        
        <p style="color: #475569; font-size: 16px; line-height: 1.6; margin: 24px 0;">
            O pagamento será processado em breve via PIX para a chave cadastrada em seu perfil.
        </p>
        
        <p style="color: #10b981; font-size: 16px; font-weight: 600;">
            Parabéns pelo trabalho! Continue assim! 🌟
        </p>
    '''
    
    enviar_email(email, f"💰 Pagamento confirmado: {trabalho_titulo}", get_email_base(conteudo))


# ============================================
# EMAILS PARA EMPRESAS
# ============================================

def email_boas_vindas_empresa(nome_fantasia, email):
    """Email de boas-vindas para nova empresa."""
    conteudo = f'''
        <h2 style="color: #1e293b; margin: 0 0 16px;">Bem-vinda, {nome_fantasia}! 🏢</h2>
        <p style="color: #475569; font-size: 16px; line-height: 1.6; margin: 0 0 24px;">
            Seu cadastro foi recebido e está em análise pela nossa equipe.
        </p>
        
        <div style="background-color: #f0f9ff; border-radius: 12px; padding: 24px; border-left: 4px solid #06b6d4;">
            <h3 style="color: #0891b2; margin: 0 0 8px;">📋 Status: Em Análise</h3>
            <p style="color: #475569; margin: 0;">
                Verificamos os dados da empresa para garantir a segurança de todos. 
                Você receberá um email assim que a análise for concluída (geralmente em até 24h).
            </p>
        </div>
        
        <div style="margin: 32px 0;">
            <h3 style="color: #1e293b; margin: 0 0 16px;">Enquanto isso, saiba o que você poderá fazer:</h3>
            <ul style="color: #475569; padding-left: 20px;">
                <li style="margin-bottom: 12px;">✅ Publicar trabalhos em minutos</li>
                <li style="margin-bottom: 12px;">✅ Receber candidaturas de universitários verificados</li>
                <li style="margin-bottom: 12px;">✅ Selecionar os melhores perfis</li>
                <li>✅ Nota fiscal emitida pela plataforma</li>
            </ul>
        </div>
    '''
    
    enviar_email(email, "🏢 Cadastro recebido - ExtraSITE", get_email_base(conteudo))


def email_empresa_aprovada(nome_fantasia, email):
    """Email notificando que empresa foi aprovada."""
    conteudo = f'''
        <h2 style="color: #10b981; margin: 0 0 16px;">Empresa Aprovada! ✅</h2>
        <p style="color: #475569; font-size: 16px; line-height: 1.6; margin: 0 0 24px;">
            Parabéns, {nome_fantasia}! Sua empresa foi aprovada e você já pode publicar trabalhos na plataforma.
        </p>
        
        <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(6, 182, 212, 0.1)); border-radius: 12px; padding: 24px; text-align: center;">
            <p style="font-size: 48px; margin: 0 0 16px;">🎉</p>
            <p style="color: #10b981; font-weight: 700; font-size: 20px; margin: 0;">
                Sua conta está ativa!
            </p>
        </div>
        
        <div style="text-align: center; margin: 32px 0;">
            <a href="https://extrasite.com/empresa/trabalho/novo" style="display: inline-block; background: linear-gradient(135deg, #7c3aed, #06b6d4); color: #ffffff; text-decoration: none; padding: 16px 32px; border-radius: 12px; font-weight: 600; font-size: 16px;">
                Publicar Primeiro Trabalho
            </a>
        </div>
    '''
    
    enviar_email(email, "✅ Empresa aprovada - ExtraSITE", get_email_base(conteudo))


def email_nova_candidatura(empresa_email, empresa_nome, colaborador_nome, trabalho_titulo):
    """Email notificando empresa sobre nova candidatura."""
    conteudo = f'''
        <h2 style="color: #1e293b; margin: 0 0 16px;">Nova Candidatura! 📩</h2>
        <p style="color: #475569; font-size: 16px; line-height: 1.6; margin: 0 0 24px;">
            Olá {empresa_nome}, você recebeu uma nova candidatura!
        </p>
        
        <div style="background-color: #f8fafc; border-radius: 12px; padding: 24px; border-left: 4px solid #7c3aed;">
            <p style="color: #64748b; margin: 0 0 8px;">Trabalho:</p>
            <h3 style="color: #1e293b; margin: 0 0 16px;">{trabalho_titulo}</h3>
            <p style="color: #64748b; margin: 0 0 4px;">Candidato:</p>
            <p style="color: #7c3aed; font-weight: 600; font-size: 18px; margin: 0;">{colaborador_nome}</p>
        </div>
        
        <div style="text-align: center; margin: 32px 0;">
            <a href="https://extrasite.com/empresa/dashboard" style="display: inline-block; background: linear-gradient(135deg, #7c3aed, #06b6d4); color: #ffffff; text-decoration: none; padding: 16px 32px; border-radius: 12px; font-weight: 600; font-size: 16px;">
                Ver Candidatura
            </a>
        </div>
        
        <p style="color: #94a3b8; font-size: 14px; text-align: center;">
            Responda em até 48h para manter um bom tempo de resposta!
        </p>
    '''
    
    enviar_email(empresa_email, f"📩 Nova candidatura: {trabalho_titulo}", get_email_base(conteudo))


# ============================================
# EMAILS ADMINISTRATIVOS
# ============================================

def email_admin_nova_empresa(admin_email, empresa_nome, cnpj):
    """Notifica admin sobre nova empresa aguardando aprovação."""
    conteudo = f'''
        <h2 style="color: #1e293b; margin: 0 0 16px;">Nova Empresa Cadastrada 🏢</h2>
        <p style="color: #475569; font-size: 16px; line-height: 1.6; margin: 0 0 24px;">
            Uma nova empresa se cadastrou e aguarda aprovação.
        </p>
        
        <div style="background-color: #f8fafc; border-radius: 12px; padding: 24px;">
            <p style="color: #64748b; margin: 0 0 8px;">Empresa:</p>
            <h3 style="color: #1e293b; margin: 0 0 8px;">{empresa_nome}</h3>
            <p style="color: #64748b; margin: 0;">CNPJ: {cnpj}</p>
        </div>
        
        <div style="text-align: center; margin: 32px 0;">
            <a href="https://extrasite.com/admin/empresas?status=aguardando_aprovacao" style="display: inline-block; background: #f59e0b; color: #ffffff; text-decoration: none; padding: 16px 32px; border-radius: 12px; font-weight: 600; font-size: 16px;">
                Revisar Cadastro
            </a>
        </div>
    '''
    
    enviar_email(admin_email, f"🏢 Nova empresa aguardando aprovação: {empresa_nome}", get_email_base(conteudo))
