# ExtraSITE - Plataforma de Freelance Universitário

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Flask-3.1.2-green.svg" alt="Flask">
  <img src="https://img.shields.io/badge/SQLite-Database-lightblue.svg" alt="SQLite">
  <img src="https://img.shields.io/badge/Status-MVP-yellow.svg" alt="Status">
</p>

---

## 📋 Sobre o Projeto

**ExtraSITE** é uma plataforma web que conecta **estudantes universitários** a **empresas locais** que precisam de mão de obra temporária para eventos e serviços diversos. O objetivo é profissionalizar o "trabalho extra" (bico) oferecendo segurança, praticidade e garantias para ambos os lados.

### 🎯 Problema que Resolvemos

| Para Empresas | Para Estudantes |
|---------------|-----------------|
| Dificuldade em encontrar mão de obra rápida | Falta de oportunidades flexíveis |
| Medo de problemas trabalhistas              | Risco de calote em acordos informais |
| Burocracia para pagar pessoas físicas       | Dificuldade de entrar no mercado |

### 💡 Nossa Solução

- **Marketplace centralizado** de serviços temporários
- **Sistema de escrow** (garantia de pagamento)
- **Substituição garantida** em caso de imprevistos
- **Emissão de nota fiscal** pela plataforma
- **Taxa transparente** configurável pelo admin

---

## 🏗️ Arquitetura do Sistema

```
extrasite/
├── app/
│   ├── __init__.py              # App Factory + Context Processors
│   ├── models/                  # Modelos SQLAlchemy
│   │   ├── colaborador.py       # Estudante/Freelancer
│   │   ├── empresa.py           # Empresa contratante
│   │   ├── trabalho.py          # Oportunidade de trabalho
│   │   ├── candidatura.py       # Candidatura a trabalho
│   │   └── admin.py             # Administrador
│   ├── routes/                  # Controllers/Blueprints
│   │   ├── main.py              # Páginas públicas
│   │   ├── auth.py              # Autenticação
│   │   ├── colaborador.py       # Área do colaborador
│   │   ├── empresa.py           # Área da empresa
│   │   └── admin.py             # Painel administrativo
│   ├── forms/                   # WTForms
│   │   ├── auth.py              # Forms de login/cadastro
│   │   ├── colaborador.py       # Forms do colaborador
│   │   └── empresa.py           # Forms da empresa
│   ├── templates/               # Templates Jinja2
│   │   ├── base.html            # Layout base
│   │   ├── main/                # Páginas públicas
│   │   ├── auth/                # Login/Cadastro
│   │   ├── colaborador/         # Área colaborador
│   │   ├── empresa/             # Área empresa
│   │   └── admin/               # Painel admin
│   ├── static/                  # Arquivos estáticos
│   │   ├── css/style.css        # Estilos (1600+ linhas)
│   │   └── uploads/             # Fotos de perfil
│   └── utils/                   # Utilitários
│       └── upload.py            # Upload de imagens
├── instance/
│   ├── extrasite.db             # Banco SQLite
│   └── platform_config.json     # Configurações dinâmicas
├── config.py                    # Configurações Flask
├── run.py                       # Ponto de entrada
├── create_admin.py              # Script criar admin
├── requirements.txt             # Dependências
├── POLITICAS.md                 # Políticas completas
└── README.md                    # Este arquivo
```

---

## 🔌 Endpoints da API

### 🌐 Rotas Públicas (`main_bp`)

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/` | Página inicial com trabalhos recentes |
| GET | `/sobre` | Página sobre a plataforma |
| GET | `/termos` | Termos de uso |
| GET | `/privacidade` | Política de privacidade |
| GET | `/cancelamento` | Política de cancelamento |

### 🔐 Autenticação (`auth_bp` - prefixo `/auth`)

| Método | Rota | Descrição |
|--------|------|-----------|
| GET/POST | `/login` | Login unificado (detecta tipo automaticamente) |
| GET/POST | `/login-admin` | Login exclusivo para admin |
| GET      | `/logout` | Logout |
| GET/POST | `/cadastro/colaborador` | Cadastro de estudante |
| GET/POST | `/cadastro/empresa` | Cadastro de empresa |

### 👤 Área do Colaborador (`colaborador_bp` - prefixo `/colaborador`)

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/dashboard` | Dashboard com trabalhos aceitos/pendentes |
| GET | `/mural` | Mural de oportunidades disponíveis |
| GET | `/trabalho/<id>` | Ver detalhes de um trabalho |
| POST | `/trabalho/<id>/candidatar` | Candidatar-se a trabalho |
| POST | `/candidatura/<id>/cancelar` | Cancelar candidatura |
| GET | `/minhas-candidaturas` | Listar todas candidaturas |
| GET/POST | `/perfil` | Editar perfil |

### 🏢 Área da Empresa (`empresa_bp` - prefixo `/empresa`)

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/dashboard` | Dashboard com estatísticas |
| GET/POST | `/trabalho/novo` | Criar novo trabalho |
| GET | `/trabalho/<id>` | Ver trabalho + candidaturas |
| POST | `/trabalho/<id>/candidatura/<id>/aceitar` | Aceitar candidatura |
| POST | `/trabalho/<id>/candidatura/<id>/recusar` | Recusar candidatura |
| POST | `/trabalho/<id>/confirmar/<id>` | Confirmar execução |
| POST | `/trabalho/<id>/nao-compareceu/<id>` | Marcar no-show |
| POST | `/trabalho/<id>/concluir` | Concluir trabalho |
| GET | `/meus-trabalhos` | Listar todos trabalhos |
| GET/POST | `/perfil` | Editar perfil empresa |

### ⚙️ Painel Admin (`admin_bp` - prefixo `/admin`)

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/dashboard` | Dashboard administrativo |
| GET | `/empresas` | Listar empresas (com filtro) |
| GET | `/empresa/<id>` | Ver detalhes empresa |
| POST | `/empresa/<id>/aprovar` | Aprovar empresa |
| POST | `/empresa/<id>/rejeitar` | Rejeitar empresa |
| GET | `/colaboradores` | Listar colaboradores |
| GET | `/colaborador/<id>` | Ver detalhes colaborador |
| GET | `/trabalhos` | Listar trabalhos |
| POST | `/trabalho/<id>/cancelar` | Cancelar trabalho |
| GET/POST | `/configuracoes` | Configurações da plataforma |

---

## 📊 Modelos de Dados

### Colaborador
```python
- id (UUID)
- nome, email, senha_hash, telefone
- universidade, foto_perfil
- bio, habilidades, experiencias (JSON)
- chave_pix
- status (ativo/pendente/suspenso)
- avaliacao_media, total_avaliacoes, total_trabalhos
- criado_em, atualizado_em
```

### Empresa
```python
- id (UUID)
- razao_social, nome_fantasia, cnpj
- email, senha_hash, telefone
- pessoa_contato
- endereco (rua, cidade, estado, cep)
- status (aguardando_aprovacao/ativo/suspenso)
- criado_em, atualizado_em
```

### Trabalho
```python
- id (UUID)
- empresa_id (FK)
- titulo, descricao, categoria, requisitos
- local_endereco, local_cidade
- data, horario_inicio, horario_fim
- valor_pagamento, valor_sugerido
- vagas_total, vagas_preenchidas
- status (rascunho/aberto/em_andamento/concluido/cancelado)
- criado_em, atualizado_em
# Propriedades calculadas:
- valor_liquido (valor - taxa)
- taxa_plataforma
- duracao_horas
- vagas_disponiveis
```

### Candidatura
```python
- id (UUID)
- trabalho_id (FK), colaborador_id (FK)
- mensagem
- status (pendente/aceita/recusada/cancelada)
- confirmado_empresa, compareceu
- candidatou_em, respondido_em
```

### Avaliação
```python
- id (UUID)
- candidatura_id (FK), trabalho_id (FK)
- avaliador_tipo (empresa/colaborador)
- avaliador_id, avaliado_tipo, avaliado_id
- nota (1-5 estrelas)
- comentario (texto livre)
- pontualidade, profissionalismo, comunicacao (1-5, opcionais)
- criado_em
# Métodos estáticos:
- empresa_ja_avaliou(candidatura_id)
- colaborador_ja_avaliou(candidatura_id)
- criar_avaliacao_empresa(candidatura, nota, ...)
- criar_avaliacao_colaborador(candidatura, nota, ...)
```

---

## ⭐ Sistema de Avaliações

Após a conclusão de um trabalho (presença confirmada), ambas as partes podem se avaliar:

### Fluxo de Avaliação
1. **Empresa confirma presença** do colaborador no trabalho
2. **Botão "⭐ Avaliar"** aparece para ambos
3. Avaliação inclui:
   - Nota geral (1-5 estrelas) - obrigatória
   - Subcategorias: Pontualidade, Profissionalismo, Comunicação (opcionais)
   - Comentário (opcional)
4. Média é automaticamente recalculada no perfil do avaliado

### Rotas de Avaliação
| Rota | Descrição |
|------|-----------|
| `/colaborador/avaliar/<id>` | Colaborador avalia empresa |
| `/empresa/avaliar/<id>` | Empresa avalia colaborador |
| `/colaborador/avaliacoes` | Ver avaliações recebidas |
| `/empresa/avaliacoes` | Ver avaliações recebidas |

---

## ⚙️ Configurações Dinâmicas

O admin pode alterar em `/admin/configuracoes`:

| Config | Descrição | Padrão |
|--------|-----------|--------|
| `PLATFORM_NAME` | Nome da plataforma | ExtraSITE |
| `PLATFORM_CITY` | Região de atuação | Medianeira - PR |
| `TAKE_RATE` | Taxa da plataforma | 15% (0.15) |
| `CANCELLATION_WINDOW_HOURS` | Janela cancelamento | 48h |
| `VALORES_SUGERIDOS` | R$/hora por categoria | Variável |
| `TERMOS_DE_USO` | Texto dos termos | HTML |
| `POLITICA_PRIVACIDADE` | Texto de privacidade | HTML |
| `POLITICA_CANCELAMENTO` | Texto de cancelamento | HTML |

Salvo em: `instance/platform_config.json`

---

## 💰 Modelo de Negócio

```
┌─────────────────────────────────────────────────────┐
│  Empresa paga:           R$ 100,00                  │
│                              │                      │
│                              ▼                      │
│  ┌──────────────────────────────────────────────┐  │
│  │         PLATAFORMA (ExtraSITE)                │  │
│  │         Taxa: 15% = R$ 15,00                  │  │
│  └──────────────────────────────────────────────┘  │
│                              │                      │
│                              ▼                      │
│  Colaborador recebe:     R$ 85,00                  │
│  (valor_liquido)                                    │
└─────────────────────────────────────────────────────┘
```

O colaborador **sempre vê o valor líquido** (após desconto).

---

## 🎨 Design System

### Cores
```css
--primary: #7c3aed (Roxo)
--secondary: #06b6d4 (Ciano)
--success: #10b981 (Verde)
--warning: #f59e0b (Amarelo)
--danger: #ef4444 (Vermelho)
```

### Componentes
- Cards com glassmorphism
- Botões com gradientes
- Badges de status
- Alertas informativos
- Grids responsivos (1, 2, 3, 4 colunas)
- Formulários estilizados

### Tipografia
- Font: Inter (Google Fonts)
- Escala: 0.875rem → 2rem

---

## 🚀 Como Executar

### Pré-requisitos
- Python 3.10+
- pip

### Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/extrasite.git
cd extrasite

# 2. Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. Instale dependências
pip install -r requirements.txt

# 4. Crie o admin
python create_admin.py

# 5. Execute
flask run
```

Acesse: http://127.0.0.1:5000

---

## 🔜 Roadmap (Próximas Features)

### Prioridade Alta
- [ ] Sistema de notificações por email
- [ ] Sistema de avaliações (estrelas)
- [ ] Sistema de penalidades automáticas
- [ ] Gateway de pagamento (Stripe/Mercado Pago)

### Prioridade Média
- [ ] Upload/troca de foto de perfil
- [ ] Verificação de identidade
- [ ] Chat entre empresa e colaborador
- [ ] Filtros avançados no mural

### Prioridade Baixa
- [ ] Dashboard com gráficos
- [ ] Exportar relatórios
- [ ] App mobile (PWA)
- [ ] Integração com calendário

---

## 📜 Políticas Implementadas

- ✅ **Termos de Uso** - 8 seções
- ✅ **Política de Privacidade** - LGPD compliant
- ✅ **Política de Cancelamento** - Com penalidades progressivas

Ver: [POLITICAS.md](POLITICAS.md)

---

## 🔐 Segurança

- Senhas hasheadas (Werkzeug)
- CSRF Protection (Flask-WTF)
- Login com Flask-Login
- Decorators de autorização por tipo de usuário
- Validação de formulários server-side

---

## 📞 Contato

- **Email:** contato@extrasite.com
- **Região:** Medianeira - PR

---

## 📄 Licença

MIT License - Veja [LICENSE](LICENSE)

---

<p align="center">
  <strong>ExtraSITE</strong> - Conectando universitários a oportunidades 🎓💼
</p>
