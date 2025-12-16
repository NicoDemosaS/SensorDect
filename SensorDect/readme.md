# 🔔 SensorDect

Sistema de monitoramento e controle de alarme via web, desenvolvido com Flask.

## 📋 Descrição

SensorDect é uma aplicação web para gerenciamento de sistema de alarme com funcionalidades de:
- Autenticação de usuários
- Dashboard de monitoramento em tempo real
- Controle remoto do alarme
- Configurações avançadas do sistema
- Atualização de firmware via OTA

## 🚀 Tecnologias Utilizadas

- **Backend:** Flask (Python)
- **Frontend:** HTML5, CSS3, JavaScript
- **Autenticação:** Flask Sessions (cookies criptografados)
- **Arquitetura:** Blueprints (modular)

## 📁 Estrutura do Projeto

```
SensorDect/
├── main.py                 # Ponto de entrada da aplicação
├── routes/                 # Módulos de rotas (Blueprints)
│   ├── __init__.py
│   ├── auth.py            # Rotas de autenticação (login/logout)
│   ├── dashboard.py       # Rota do dashboard
│   ├── config.py          # Rota de configurações
│   └── alarm.py           # API do alarme (ativar/desativar/status)
├── templates/             # Templates HTML
│   ├── index.html         # Página de login
│   ├── dashboard.html     # Dashboard principal
│   └── config.html        # Página de configurações
└── readme.md
```

## ✨ Funcionalidades Implementadas

### 🔐 Autenticação (`auth.py`)
- **Login:** Sistema de autenticação com sessões
- **Logout:** Encerramento de sessão
- **Proteção de rotas:** Apenas usuários autenticados acessam páginas internas

### 📊 Dashboard (`dashboard.html`)
- **Status Online/Offline:** Indicador em tempo real do sistema
- **Último Evento:** Data e hora do último evento registrado
- **Indicadores:**
  - Nível de bateria (%)
  - Intensidade do sinal WiFi (%)
- **Gráfico de Ativações:** 
  - Visualização por horário (hoje)
  - Visualização por dia (semana)
  - Visualização por semana (mês)
- **Botão de Configurações:** Acesso rápido às configurações

### ⚙️ Configurações (`config.html`)
- **Controle do Alarme:**
  - Ativar/Desativar alarme principal
  - Modo silencioso (silent mode)
  - Ajuste de sensibilidade (baixa/média/alta)
  - Configuração do tempo de alarme (segundos)
- **Manutenção:**
  - Reset remoto do dispositivo
  - Atualização de firmware via OTA (Over-The-Air)
  - Verificação de atualizações disponíveis

### 🔔 API do Alarme (`alarm.py`)
- `POST /ativar-alarme` - Ativa o sistema de alarme
- `POST /desativar-alarme` - Desativa o sistema de alarme
- `GET /status-alarme` - Retorna o status atual do alarme

## 🔧 Instalação

### Pré-requisitos
- Python 3.8+
- pip

### Passos

1. **Clone o repositório:**
```bash
git clone <url-do-repositorio>
cd SensorDect
```

2. **Crie um ambiente virtual (recomendado):**
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Instale as dependências:**
```bash
pip install flask
```

4. **Execute a aplicação:**
```bash
python3 main.py
```

5. **Acesse no navegador:**
```
http://localhost:5000
```

## 🔑 Credenciais Padrão

- **Usuário:** admin
- **Senha:** admin

> ⚠️ **Importante:** Altere as credenciais em produção!

## 🛠️ Configuração

### Secret Key
A aplicação usa uma `secret_key` para criptografar sessões. Em produção, use uma chave forte:

```python
# main.py
app.secret_key = 'sua_chave_secreta_super_segura_aqui'
```

Ou use variáveis de ambiente:
```python
import os
app.secret_key = os.environ.get('SECRET_KEY', 'fallback_key')
```

## 📡 Rotas Disponíveis

### Páginas
- `/` - Redireciona para login ou dashboard
- `/login` - Página de login
- `/logout` - Encerra sessão
- `/dashboard` - Dashboard principal (requer autenticação)
- `/config` - Página de configurações (requer autenticação)

### API
- `POST /ativar-alarme` - Ativa o alarme
- `POST /desativar-alarme` - Desativa o alarme
- `GET /status-alarme` - Status do alarme

## 🎨 Design

O projeto utiliza um design moderno e responsivo com:
- Gradientes roxos/azuis
- Animações suaves
- Cards interativos
- Interface intuitiva
- Layout responsivo para mobile

## 🔒 Segurança

- **Sessions:** Cookies criptografados com `secret_key`
- **Proteção de rotas:** Todas as páginas internas verificam autenticação
- **Redirecionamento:** Usuários não autenticados são redirecionados ao login

## 🚧 Próximas Funcionalidades

- [ ] Banco de dados para persistência de usuários
- [ ] Hash de senhas (bcrypt/werkzeug)
- [ ] Histórico de eventos
- [ ] Notificações em tempo real (WebSocket)
- [ ] Integração com hardware (ESP32/Arduino)
- [ ] Múltiplos usuários e permissões
- [ ] Logs de atividades
- [ ] API REST completa

## 📝 Notas de Desenvolvimento

### Blueprints
O projeto usa **Blueprints** do Flask para modularizar as rotas:
- Cada módulo de funcionalidade tem seu próprio arquivo
- Facilita manutenção e escalabilidade
- Código organizado e reutilizável

### Sessions
O sistema de autenticação usa **Flask Sessions**:
- Armazena dados do usuário em cookies criptografados
- Não requer banco de dados para autenticação básica
- Seguro quando usado com `secret_key` forte

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## 📄 Licença

Este projeto está sob a licença MIT.

## 👤 Autor

Desenvolvido por Maquiavels

---

**SensorDect** - Sistema de Monitoramento e Controle de Alarme 🔔
