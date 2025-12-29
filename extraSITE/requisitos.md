# Requisitos do Sistema - Plataforma de Freelance Universitário

**Documento:** Especificação de Requisitos (MVP)  
**Versão:** 1.0  
**Data:** 2025-12-19  
**Referência:** [visao.md](./visao.md)

---

## 1. Visão Geral do MVP

### 1.1 Escopo
Plataforma web responsiva para conectar **colaboradores** (estudantes universitários) a **empresas** que precisam de mão de obra para **eventos** na região de **Medianeira - PR**.

### 1.2 Tipos de Usuário
| Tipo | Descrição |
|------|-----------|
| **Colaborador** | Estudante universitário que busca trabalhos temporários |
| **Empresa** | Pessoa jurídica (CNPJ) que publica trabalhos |
| **Admin** | Administrador da plataforma (aprovação de empresas, gestão) |

### 1.3 Stack Tecnológica
- **Backend:** Flask (Python)
- **Frontend:** Web responsivo (templates Jinja2 ou SPA futura)
- **Banco de Dados:** PostgreSQL
- **Pagamentos:** A definir (Asaas, Pagar.me ou Stripe) — *implementação posterior*

---

## 2. Entidades do Sistema

### 2.1 Colaborador (Estudante)

#### Campos do Cadastro
| Campo | Tipo | Obrigatório | Observação |
|-------|------|-------------|------------|
| `id` | UUID | Auto | Chave primária |
| `nome` | String | ✅ | Nome completo |
| `email` | String | ✅ | Preferencialmente `.edu` para validação universitária |
| `senha` | String (hash) | ✅ | Autenticação |
| `telefone` | String | ✅ | WhatsApp para contato |
| `universidade` | String | ✅ | Instituição de ensino |
| `foto_perfil` | URL | ✅ | Foto obrigatória |
| `bio` | Text | ❌ | Descrição livre sobre si |
| `habilidades` | Text | ❌ | Texto livre (ex: "experiência com atendimento") |
| `experiencias` | JSON/Text | ❌ | Lista estruturada mas não obrigatória |
| `chave_pix` | String | ❌ | Cadastra depois, quando for receber |
| `status` | Enum | Auto | `pendente`, `ativo`, `suspenso` |
| `criado_em` | Timestamp | Auto | |

#### Experiências (estrutura sugerida)
```json
[
  {
    "descricao": "Garçom em evento de formatura",
    "local": "Buffet XYZ",
    "periodo": "2024"
  }
]
```
> **Nota:** Preenchimento opcional e flexível, sem burocracia.

---

### 2.2 Empresa

#### Campos do Cadastro
| Campo | Tipo | Obrigatório | Observação |
|-------|------|-------------|------------|
| `id` | UUID | Auto | Chave primária |
| `email` | String | ✅ | Login |
| `senha` | String (hash) | ✅ | Autenticação |
| `razao_social` | String | ✅ | Nome legal |
| `nome_fantasia` | String | ✅ | Nome comercial |
| `cnpj` | String | ✅ | Validado, único |
| `telefone` | String | ✅ | Contato principal |
| `endereco` | JSON | ✅ | `{rua, cidade, estado, cep}` |
| `pessoa_contato` | String | ✅ | Nome do responsável |
| `logo` | URL | ❌ | Logo da empresa |
| `avaliacao_media` | Decimal | Auto | Calculado das avaliações (futuro) |
| `status` | Enum | Auto | `aguardando_aprovacao`, `ativo`, `suspenso` |
| `aprovado_por` | FK → Admin | — | Quem aprovou |
| `aprovado_em` | Timestamp | — | Data da aprovação |
| `criado_em` | Timestamp | Auto | |

> **Regra:** Empresa só pode publicar trabalhos após aprovação do Admin.

---

### 2.3 Trabalho (Gig)

#### Campos
| Campo | Tipo | Obrigatório | Observação |
|-------|------|-------------|------------|
| `id` | UUID | Auto | Chave primária |
| `empresa_id` | FK → Empresa | ✅ | Quem publicou |
| `titulo` | String | ✅ | Ex: "Garçom para casamento" |
| `descricao` | Text | ✅ | Detalhes do serviço |
| `categoria` | Enum | ✅ | Ver lista abaixo |
| `local` | JSON | ✅ | `{endereco, cidade}` |
| `data` | Date | ✅ | Dia do trabalho |
| `horario_inicio` | Time | ✅ | |
| `horario_fim` | Time | ✅ | |
| `valor_pagamento` | Decimal | ✅ | Valor por colaborador |
| `valor_sugerido` | Decimal | Auto | Sugestão da plataforma (referência) |
| `vagas_total` | Integer | ✅ | Quantos colaboradores precisa |
| `vagas_preenchidas` | Integer | Auto | Contador |
| `requisitos` | Text | ❌ | Ex: "Ter roupa social preta" |
| `status` | Enum | Auto | Ver estados abaixo |
| `criado_em` | Timestamp | Auto | |

#### Categorias de Trabalho (MVP)
| Código | Descrição |
|--------|-----------|
| `garcom` | Garçom |
| `bartender` | Bartender |
| `organizacao` | Organizador de Eventos |

> **Expansão futura:** Carga/descarga, limpeza, recepção, etc.

#### Estados do Trabalho
```
[rascunho] → [aberto] → [em_andamento] → [concluido]
                 ↓              ↓
            [cancelado]    [cancelado]
```

| Status | Descrição |
|--------|-----------|
| `rascunho` | Empresa ainda editando (não publicado) |
| `aberto` | Publicado, aceitando candidaturas |
| `em_andamento` | Data chegou, serviço sendo executado |
| `concluido` | Empresa confirmou execução |
| `cancelado` | Cancelado (por empresa ou falta de candidatos) |

---

### 2.4 Candidatura

#### Campos
| Campo | Tipo | Obrigatório | Observação |
|-------|------|-------------|------------|
| `id` | UUID | Auto | |
| `trabalho_id` | FK → Trabalho | ✅ | |
| `colaborador_id` | FK → Colaborador | ✅ | |
| `mensagem` | Text | ❌ | Recado opcional do colaborador |
| `status` | Enum | Auto | `pendente`, `aceita`, `recusada`, `cancelada` |
| `candidatou_em` | Timestamp | Auto | |
| `respondido_em` | Timestamp | — | Quando empresa decidiu |

#### Regras de Candidatura
- Colaborador pode se candidatar a **múltiplos trabalhos**, mesmo com horários conflitantes.
- Quando uma candidatura é **aceita**, o sistema **cancela automaticamente** outras candidaturas do mesmo colaborador que conflitem no horário.
- Empresa seleciona colaboradores **individualmente** (um por um).

---

### 2.5 Admin

#### Campos
| Campo | Tipo | Obrigatório |
|-------|------|-------------|
| `id` | UUID | Auto |
| `nome` | String | ✅ |
| `email` | String | ✅ |
| `senha` | String (hash) | ✅ |
| `criado_em` | Timestamp | Auto |

---

## 3. Fluxos do Sistema

### 3.1 Cadastro do Colaborador

```
┌─────────────────────────────────────────────────────────┐
│  1. Acessa página de cadastro                           │
│  2. Preenche: nome, email (.edu), senha, telefone,      │
│     universidade, foto de perfil                        │
│  3. (Opcional) Adiciona bio, habilidades, experiências  │
│  4. Confirma email (link de verificação)                │
│  5. Conta ativa → pode navegar e se candidatar          │
└─────────────────────────────────────────────────────────┘
```

---

### 3.2 Cadastro da Empresa

```
┌─────────────────────────────────────────────────────────┐
│  1. Acessa página de cadastro empresarial               │
│  2. Preenche: email, senha, razão social, nome          │
│     fantasia, CNPJ, telefone, endereço, contato         │
│  3. Sistema valida formato do CNPJ                      │
│  4. Status: "aguardando_aprovacao"                      │
│  5. Admin recebe notificação de nova empresa            │
│  6. Admin aprova ou rejeita no painel                   │
│  7. Se aprovada → status "ativo", pode publicar         │
└─────────────────────────────────────────────────────────┘
```

---

### 3.3 Publicação de Trabalho

```
┌─────────────────────────────────────────────────────────┐
│  1. Empresa (aprovada) acessa "Publicar Trabalho"       │
│  2. Preenche: título, descrição, categoria, local,      │
│     data, horário, valor, quantidade de vagas           │
│  3. Sistema exibe valor sugerido como referência        │
│  4. Empresa define valor final (pode ser diferente)     │
│  5. Empresa realiza pagamento (escrow)                  │
│     → Valor total = valor_unitário × vagas_total        │
│  6. Trabalho publicado → status "aberto"                │
│  7. Aparece no Mural para colaboradores                 │
└─────────────────────────────────────────────────────────┘
```

---

### 3.4 Candidatura e Seleção

```
COLABORADOR                 PLATAFORMA                    EMPRESA
     │                          │                            │
     │  1. Navega no Mural      │                            │
     │     (filtros: categoria, │                            │
     │      data, cidade)       │                            │
     │                          │                            │
     │  2. Visualiza trabalho   │                            │
     │     (vê empresa, nota,   │                            │
     │      valor, detalhes)    │                            │
     │                          │                            │
     │  3. Se candidata         │                            │
     │ ─────────────────────────►                            │
     │                          │  4. Notifica empresa       │
     │                          │ ───────────────────────────►
     │                          │                            │
     │                          │  5. Empresa vê candidatos  │
     │                          │     (perfil, foto, exp.)   │
     │                          │                            │
     │                          │  6. Aceita/Recusa cada um  │
     │                          │ ◄───────────────────────────
     │                          │                            │
     │  7. Notificado da        │                            │
     │     decisão              │                            │
     │ ◄─────────────────────────                            │
     │                          │                            │
     │  [Se aceito]             │                            │
     │  8. Candidaturas         │                            │
     │     conflitantes são     │                            │
     │     canceladas auto.     │                            │
```

---

### 3.5 Execução e Confirmação

```
┌─────────────────────────────────────────────────────────┐
│  1. Dia do trabalho chega                               │
│  2. Colaborador executa o serviço                       │
│  3. Empresa acessa o trabalho no sistema                │
│  4. Empresa clica em "Confirmar Execução" para cada     │
│     colaborador que compareceu                          │
│  5. Se alguém faltou → marca como "não compareceu"      │
│  6. Pagamento liberado para quem foi confirmado         │
│  7. Reembolso proporcional para vagas não preenchidas   │
│     ou colaboradores que faltaram                       │
└─────────────────────────────────────────────────────────┘
```

---

### 3.6 Cancelamento e Penalidades

#### Regra dos 48h
| Quem cancela | Quando | Consequência |
|--------------|--------|--------------|
| Colaborador | ≥ 48h antes | Sem penalidade |
| Colaborador | < 48h antes | ⚠️ **Penalidade (a definir)** |
| Empresa | ≥ 48h antes | Reembolso total |
| Empresa | < 48h antes | ⚠️ **Penalidade (a definir)** |

> **TODO:** Definir valores/regras específicas das penalidades.

---

## 4. Painel Admin

### 4.1 Funcionalidades do MVP

- [ ] **Login seguro** (autenticação separada)
- [ ] **Dashboard** com métricas básicas:
  - Empresas aguardando aprovação
  - Trabalhos ativos
  - Total de colaboradores
- [ ] **Gestão de Empresas:**
  - Listar empresas (filtro por status)
  - Ver detalhes da empresa
  - Aprovar / Rejeitar empresa
  - Suspender empresa
- [ ] **Gestão de Colaboradores:**
  - Listar colaboradores
  - Ver perfil
  - Suspender colaborador
- [ ] **Gestão de Trabalhos:**
  - Listar trabalhos
  - Ver detalhes
  - Cancelar trabalho (em caso de problema)

---

## 5. Filtros do Mural (Colaborador)

O colaborador pode filtrar trabalhos por:

| Filtro | Tipo | Exemplo |
|--------|------|---------|
| Categoria | Select | Garçom, Bartender, Organização |
| Cidade | Select/Text | Medianeira, Foz do Iguaçu, região |
| Data | Date range | Próximos 7 dias, mês, específico |
| Valor mínimo | Number | A partir de R$ 100 |

---

## 6. Regras de Negócio Importantes

### 6.1 Validação Universitária
- Email `.edu` é **preferencial** mas não bloqueante no MVP
- Carteirinha é **opcional** (pode gerar badge "Verificado" no futuro)

### 6.2 Preço Sugerido
- Plataforma sugere valor baseado na categoria e duração
- Empresa pode definir valor diferente (para cima ou para baixo)
- Colaborador **não pode negociar** — aceita ou não se candidata

### 6.3 Escrow (Pagamento Antecipado)
- Empresa paga **no momento da publicação**
- Valor fica retido até confirmação de execução
- Reembolso automático se trabalho não for preenchido ou for cancelado

### 6.4 Take Rate (Taxa da Plataforma)
- **15%** sobre o valor do serviço (conforme visão)
- Exemplo: Trabalho de R$ 100 → Plataforma fica com R$ 15, Colaborador recebe R$ 85

---

## 7. Telas Principais (MVP)

### 7.1 Área Pública
- [ ] Landing page (apresentação da plataforma)
- [ ] Login (colaborador / empresa)
- [ ] Cadastro Colaborador
- [ ] Cadastro Empresa

### 7.2 Área do Colaborador
- [ ] Dashboard (trabalhos aceitos, próximos)
- [ ] Mural de Trabalhos (com filtros)
- [ ] Detalhes do Trabalho
- [ ] Minhas Candidaturas
- [ ] Meu Perfil (editar dados)
- [ ] Histórico de Trabalhos

### 7.3 Área da Empresa
- [ ] Dashboard (trabalhos publicados, status)
- [ ] Publicar Trabalho
- [ ] Meus Trabalhos (lista)
- [ ] Detalhes do Trabalho + Candidaturas
- [ ] Perfil da Empresa (editar)
- [ ] Histórico

### 7.4 Painel Admin
- [ ] Login Admin
- [ ] Dashboard
- [ ] Empresas (listar, aprovar, suspender)
- [ ] Colaboradores (listar, suspender)
- [ ] Trabalhos (listar, cancelar)

---

## 8. Itens para Definir Posteriormente

| Item | Status | Prioridade |
|------|--------|------------|
| Valor específico das penalidades | 🟡 A definir | Média |
| Gateway de pagamento (Asaas/Stripe/Pagar.me) | 🟡 A definir | Alta (pós-MVP) |
| Sistema de avaliação bilateral | 🟡 Versão futura | Baixa |
| Notificações (email/push) | 🟡 A definir | Média |
| App mobile | 🟡 Versão futura | Baixa |

---

## 9. Próximos Passos

1. [ ] Validar este documento de requisitos
2. [ ] Criar diagrama de banco de dados (ERD)
3. [ ] Configurar projeto Flask + PostgreSQL
4. [ ] Implementar autenticação (Colaborador, Empresa, Admin)
5. [ ] Implementar CRUD de cada entidade
6. [ ] Desenvolver fluxo de candidatura
7. [ ] Construir painel admin
8. [ ] Testes e validação
9. [ ] Deploy MVP

---

*Documento criado em 2025-12-19 — Projeto Plataforma de Freelance Universitário*
