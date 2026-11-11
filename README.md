# Portal de Solicitações — Django

Aplicação web em **Python / Django** para organizar solicitações, aprovações
e acompanhamento de trabalho por perfis de acesso. Inclui dashboards,
catálogo de dispositivos e registro de auditoria.

## Leitura rápida

| O que revisar | Arquivo ou diretório |
|---|---|
| Modelos e fluxo de solicitações | [portal/models.py](portal/models.py) e [portal/views.py](portal/views.py) |
| Login e gestão de contas | [accounts/](accounts/) |
| Diretório de usuários de demonstração | [accounts/directory.py](accounts/directory.py) |
| Rotas da aplicação | [config/urls.py](config/urls.py) e [portal/urls.py](portal/urls.py) |
| Interface e dashboards | [templates/portal/](templates/portal/) |
| Dependências | [requirements.txt](requirements.txt) |

O diretório público de usuários utiliza nomes, e-mails e identificadores
fictícios, conforme documentado em `accounts/directory.py`.
Esta versão está configurada para desenvolvimento local com SQLite e `DEBUG=True`.

## Funcionalidades

- Perfis Admin, Solicitante, Projetista e Dispositivos.
- Abertura, acompanhamento e transições do fluxo de solicitações.
- Dashboards por perfil e consulta de dispositivos.
- Registro de ações para auditoria.

## Executar localmente

Use **Python 3.12 ou superior**, compatível com a versão de Django fixada
nas dependências. O passo a passo abaixo usa apenas o computador local.

```bash
git clone https://github.com/enggusttavomn/gv-proj-portal-de-solicitacoes.git
cd gv-proj-portal-de-solicitacoes
python -m venv .venv
```

Ative o ambiente:

| Sistema | Comando |
|---|---|
| Windows PowerShell | `.\.venv\Scripts\Activate.ps1` |
| Linux / macOS | `source .venv/bin/activate` |

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py check
```

O banco `db.sqlite3` é criado localmente pelas migrações; ele não faz parte
dos arquivos versionados desta versão.

### Dados de demonstração

Em um banco local descartável, execute:

```bash
python seed_users.py
python seed_solicitacoes.py
```

O primeiro script cria os grupos e usuários do catálogo de demonstração.
Ele também redefine as senhas desses usuários quando executado novamente.
Consulte os identificadores e a senha de demonstração em
[accounts/directory.py](accounts/directory.py).

Para criar um superusuário local com credenciais próprias:

```bash
python manage.py createsuperuser
```

### Iniciar o portal

```bash
python manage.py runserver 127.0.0.1:8000
```

Abra <http://127.0.0.1:8000/accounts/login>.

Para comparar os perfis em sessões separadas, abra três terminais com o
ambiente ativado e execute um comando em cada:

```bash
python manage.py runserver 127.0.0.1:8000
python manage.py runserver 127.0.0.2:8001
python manage.py runserver 127.0.0.3:8002
```

| Perfil para demonstração | Endereço |
|---|---|
| Admin | <http://127.0.0.1:8000/accounts/login> |
| Solicitante | <http://127.0.0.2:8001/accounts/login> |
| Projetista | <http://127.0.0.3:8002/accounts/login> |

As portas permitem separar as sessões. As permissões dependem do usuário
autenticado e dos grupos, não apenas do endereço usado.

## Estado e próximos passos

- `python manage.py check` verifica a configuração; não substitui testes dos fluxos.
- As configurações atuais usam chave de desenvolvimento e `DEBUG=True`.
  Uma implantação requer configuração de produção e credenciais próprias.
- A avaliação funcional deve usar dados fictícios em um banco local.
- Não há uma demonstração hospedada indicada neste repositório.

## Contexto e autoria

Versão pessoal do projeto GV_PROJ mantida por Gustavo Nascimento.
O histórico de commits preserva as contribuições registradas no repositório.
