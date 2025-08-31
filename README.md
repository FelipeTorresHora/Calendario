# 📅 Calendário - Sistema de Gerenciamento de Tarefas

<div align="center">

[![Django](https://img.shields.io/badge/Django-5.1.2-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Ready-blue.svg)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-Cache-red.svg)](https://redis.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

Um sistema moderno de gerenciamento de tarefas e objetivos com foco em produtividade pessoal. Desenvolvido com Django, oferece uma experiência completa de organização com autenticação social, temas personalizáveis e visualizações avançadas.

## ✨ Funcionalidades Principais

### 🚀 Experiência de Usuário Moderna
- **Tela de Login Redesignada**: Interface moderna com gradientes, animações e validação em tempo real
- **Autenticação Social**: Login com Google e GitHub via OAuth2
- **Modo Escuro/Claro**: Tema adaptável com transições suaves
- **Design Responsivo**: Otimizado para desktop e mobile
- **PWA Ready**: Experiência de aplicativo nativo

### 🎯 Gerenciamento de Objetivos
- **Cave Mode Dashboard**: Visualização focada em objetivos e progresso pessoal
- **Objetivos Personalizados**: Criação e acompanhamento de metas de longo prazo
- **Streak Counter**: Contador de sequências para manter consistência
- **Heatmap de Atividades**: Visualização estilo GitHub do progresso diário

### 📋 Sistema de Tarefas Inteligente
- **Calendário Expandido**: Visualização completa de tarefas por período
- **Tarefas por Objetivo**: Vinculação de tarefas a objetivos específicos
- **Quick Add**: Adição rápida de tarefas com modal otimizado
- **Estados Visuais**: Feedback imediato para conclusão de tarefas
- **Filtros Avançados**: Organização por data, status e categoria

### 🔐 Segurança e Autenticação
- **Múltiplas Opções de Login**: Email/senha, Google e GitHub
- **Reset de Senha**: Sistema completo de recuperação de conta
- **Validação Robusta**: Proteção contra ataques comuns
- **Sessões Seguras**: Gerenciamento otimizado de sessões

### ⚡ Performance e Cache
- **Redis Cache**: Sistema de cache para melhor performance
- **Lazy Loading**: Carregamento otimizado de recursos
- **Compressão de Assets**: Arquivos estáticos otimizados
- **Database Optimization**: Queries otimizadas com select_related

## 🛠️ Stack Tecnológica

### Backend
- **Django 5.1.2**: Framework web robusto e escalável
- **PostgreSQL**: Banco de dados relacional para dados críticos
- **Redis**: Cache e gerenciamento de sessões
- **Django Allauth**: Autenticação social e tradicional
- **WhiteNoise**: Servir arquivos estáticos em produção

### Frontend
- **HTML5/CSS3**: Marcação semântica e estilos modernos
- **JavaScript ES6+**: Interatividade e validações client-side
- **CSS Variables**: Tema dinâmico e responsivo
- **Font Awesome**: Ícones vetoriais
- **SVG Graphics**: Gráficos escaláveis para diferentes telas

### DevOps e Deploy
- **Gunicorn**: Servidor WSGI para produção
- **Render/Heroku**: Plataformas de deploy suportadas
- **Docker Ready**: Containerização opcional
- **Environment Variables**: Configuração segura

## 🚀 Início Rápido

### Pré-requisitos
- Python 3.11+
- PostgreSQL 12+
- Redis (opcional, mas recomendado)
- Git

### Instalação Local

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/calendario.git
cd calendario
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente**
```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite o arquivo .env com suas configurações
```

5. **Execute as migrações**
```bash
python manage.py migrate
```

6. **Crie um superusuário**
```bash
python manage.py createsuperuser
```

7. **Execute o servidor de desenvolvimento**
```bash
python manage.py runserver
```

Acesse `http://localhost:8000` para ver a aplicação funcionando!

## ⚙️ Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
# Configurações Django
SECRET_KEY=sua-chave-secreta-super-complexa-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Banco de Dados (PostgreSQL)
DATABASE_URL=postgresql://usuario:senha@localhost:5432/calendario_db
# OU configure individualmente:
DB_NAME=nome_do_banco
DB_USER=usuario_do_banco
DB_PASSWORD=senha_do_banco
DB_HOST=localhost
DB_PORT=5432

# Redis (Opcional)
REDIS_URL=redis://localhost:6379/1

# OAuth2 - Google (Opcional)
GOOGLE_CLIENT_ID=seu-google-client-id
GOOGLE_CLIENT_SECRET=seu-google-client-secret

# OAuth2 - GitHub (Opcional)
GITHUB_CLIENT_ID=seu-github-client-id
GITHUB_CLIENT_SECRET=seu-github-client-secret

# Email (Para reset de senha)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=sua-senha-de-app
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=seu-email@gmail.com
```

### Configuração OAuth2

#### Google OAuth2
1. Acesse o [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um projeto ou selecione um existente
3. Habilite a Google+ API
4. Configure a tela de consentimento OAuth
5. Crie credenciais OAuth 2.0 Client ID
6. Adicione `http://localhost:8000/accounts/google/login/callback/` às URLs autorizadas

#### GitHub OAuth2
1. Acesse [GitHub Developer Settings](https://github.com/settings/developers)
2. Crie uma nova OAuth App
3. Configure Homepage URL: `http://localhost:8000`
4. Configure Authorization callback URL: `http://localhost:8000/accounts/github/login/callback/`

## 🚀 Deploy

### Deploy no Render

1. **Fork este repositório**

2. **Conecte ao Render**
   - Crie uma conta no [Render](https://render.com)
   - Conecte seu repositório GitHub

3. **Configure as Variáveis de Ambiente**
   ```
   SECRET_KEY=[gerar automaticamente]
   DEBUG=False
   DATABASE_URL=[conectar banco PostgreSQL do Render]
   REDIS_URL=[conectar Redis do Render - opcional]
   ```

4. **Deploy Automático**
   - O arquivo `render.yaml` já está configurado
   - Deploy automático a cada push na branch main

### Deploy no Heroku

1. **Instale o Heroku CLI**

2. **Faça o deploy**
```bash
heroku create seu-app-calendario
heroku addons:create heroku-postgresql:hobby-dev
heroku addons:create heroku-redis:hobby-dev
heroku config:set SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
heroku config:set DEBUG=False
git push heroku main
heroku run python manage.py migrate
```

## 📂 Estrutura do Projeto

```
calendario/
├── 📁 calendario/                 # App principal Django
│   ├── 📄 models.py              # Modelos de dados
│   ├── 📄 views.py               # Views e lógica de negócio
│   ├── 📄 forms.py               # Formulários Django
│   ├── 📄 urls.py                # URLs do app
│   ├── 📄 admin.py               # Interface administrativa
│   ├── 📄 cache_utils.py         # Utilitários de cache
│   └── 📁 templates/             # Templates HTML
│       ├── 📁 account/           # Templates do allauth
│       └── 📁 calendario/        # Templates do app
├── 📁 calendario_config/         # Configurações Django
│   ├── 📄 settings.py            # Configurações principais
│   ├── 📄 urls.py                # URLs globais
│   ├── 📄 wsgi.py                # WSGI para produção
│   └── 📄 asgi.py                # ASGI para funcionalidades async
├── 📁 static/                    # Arquivos estáticos fonte
│   ├── 📁 css/                   # Folhas de estilo
│   └── 📁 js/                    # JavaScript
├── 📁 staticfiles/               # Arquivos estáticos coletados
├── 📄 manage.py                  # Utilitário Django
├── 📄 requirements.txt           # Dependências Python
├── 📄 runtime.txt                # Versão Python (deploy)
├── 📄 render.yaml                # Configuração Render
├── 📄 build.sh                   # Script de build
└── 📄 README.md                  # Documentação
```

## 🧪 Testes

Execute os testes com:

```bash
# Todos os testes
python manage.py test

# Testes específicos
python manage.py test calendario.tests

# Com coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. **Fork o projeto**
2. **Crie uma branch para sua feature**
   ```bash
   git checkout -b feature/nova-funcionalidade
   ```
3. **Commit suas mudanças**
   ```bash
   git commit -m 'Adiciona nova funcionalidade'
   ```
4. **Push para a branch**
   ```bash
   git push origin feature/nova-funcionalidade
   ```
5. **Abra um Pull Request**

### Padrões de Código

- Siga a PEP 8 para Python
- Use nomes descritivos para variáveis e funções
- Comente código complexo
- Adicione testes para novas funcionalidades
- Mantenha as dependências atualizadas

### Comandos Úteis para Desenvolvimento

```bash
# Verificar problemas no código
python manage.py check

# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Coletar arquivos estáticos
python manage.py collectstatic

# Shell interativo
python manage.py shell

# Criar dados de exemplo
python manage.py loaddata fixtures/sample_data.json
```

## 📊 Roadmap

### 🎯 Próximas Funcionalidades
- [ ] **API REST**: Endpoints para integração com apps móveis
- [ ] **Notificações Push**: Lembretes e alertas
- [ ] **Colaboração**: Compartilhamento de objetivos e tarefas
- [ ] **Analytics**: Relatórios detalhados de produtividade
- [ ] **Integração Calendário**: Sync com Google Calendar/Outlook
- [ ] **Gamificação**: Sistema de pontos e conquistas
- [ ] **App Mobile**: Versões iOS e Android
- [ ] **Widgets**: Widgets personalizáveis para dashboard

### 🔧 Melhorias Técnicas
- [ ] **WebSocket**: Updates em tempo real
- [ ] **Background Tasks**: Processamento assíncrono com Celery
- [ ] **Elasticsearch**: Busca avançada
- [ ] **Docker**: Containerização completa
- [ ] **CI/CD**: Pipeline automatizado de deploy
- [ ] **Monitoring**: Logs e métricas com Sentry
- [ ] **Performance**: Otimizações adicionais de cache

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🆘 Suporte

Se você encontrar problemas ou tiver dúvidas:

1. **Verifique as Issues existentes** no GitHub
2. **Crie uma nova Issue** se necessário
3. **Consulte a documentação** do Django e das dependências
4. **Entre em contato** através das issues do projeto

## 🎉 Agradecimentos

- **Django Team** - Framework incrível
- **Django Allauth** - Sistema de autenticação completo
- **Font Awesome** - Ícones vetoriais
- **Render/Heroku** - Plataformas de deploy
- **Contribuidores** - Todos que ajudaram no desenvolvimento

---

<div align="center">

**⭐ Se este projeto foi útil, considere dar uma estrela no GitHub!**

Feito com ❤️ e ☕ por [Seu Nome](https://github.com/seu-usuario)

</div>