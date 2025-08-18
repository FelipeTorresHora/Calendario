# Calendário - Task Management App

## Deploy no Render

### 1. Configuração do Supabase
1. Acesse seu projeto no [Supabase](https://supabase.com)
2. Vá em Settings > Database > Connection pooling
3. Anote os seguintes dados:
   - Database name
   - User
   - Password  
   - Host
   - Port (geralmente 5432)

### 2. Deploy no Render
1. Faça fork/clone deste repositório
2. Conecte o repositório ao [Render](https://render.com)
3. Crie um novo Web Service
4. Use as configurações do arquivo `render.yaml` (Blueprint)

### 3. Variáveis de Ambiente no Render
Configure estas variáveis no painel do Render:

```
SECRET_KEY=your-secret-key-here
DEBUG=False
DB_NAME=your-supabase-db-name
DB_USER=your-supabase-user
DB_PASSWORD=your-supabase-password
DB_HOST=your-supabase-host.supabase.co
DB_PORT=5432
```

**Opcional (Redis):**
```
REDIS_URL=redis://your-redis-url
```

### 4. Comandos Importantes

**Desenvolvimento Local:**
```bash
# Instalar dependências
pip install -r requirements.txt

# Migrar banco
python manage.py migrate

# Executar servidor
python manage.py runserver
```

**Produção no Render:**
- Build: `./build.sh` (automático)
- Start: `gunicorn calendario_config.wsgi:application` (automático)

### 5. Funcionalidades

- **Dashboard**: Página principal com objetivos e heatmap de atividades
- **Calendário**: Visualização expandida de todas as tarefas
- **Objetivos**: Controle completo de tarefas e desafios
- **Autenticação**: Sistema de usuários com email
- **PostgreSQL**: Database Supabase
- **Redis**: Cache (opcional)

### 6. Estrutura do Projeto

```
├── calendario/           # App principal
├── calendario_config/    # Configurações Django
├── static/              # Arquivos estáticos
├── requirements.txt     # Dependências Python
├── render.yaml         # Configuração Render
├── build.sh           # Script de build
└── runtime.txt        # Versão Python
```

### 7. Deploy Automático

O projeto está configurado para deploy automático no Render:
- Cada push na branch principal irá disparar um novo deploy
- Migrações são executadas automaticamente
- Arquivos estáticos são coletados automaticamente

### 8. Troubleshooting

**Erro de conexão com banco:**
- Verifique as credenciais do Supabase
- Confirme que o SSL está habilitado no Supabase
- Teste a conexão localmente primeiro

**Erro de static files:**
- Execute `python manage.py collectstatic` localmente
- Verifique se WhiteNoise está instalado

**Erro 500 em produção:**
- Verifique os logs no painel do Render
- Confirme que DEBUG=False
- Verifique SECRET_KEY