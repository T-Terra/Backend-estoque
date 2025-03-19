# 📦 API de Cadastro de Peças

Este é o backend de um sistema de cadastro de peças automotivas, desenvolvido com **Django REST Framework**. Ele fornece autenticação JWT, controle de peças e comunicação segura com o frontend.

## 🚀 Tecnologias Utilizadas
- **Django** (5.1.7)
- **Django REST Framework** (3.15.2)
- **Python Dotenv** (1.0.1)
- **Gunicorn** (23.0.0) - Servidor WSGI
- **Psycopg2** (2.9.10) - Conector PostgreSQL
- **Simple JWT** (5.5.0) - Autenticação via JWT
- **Django CORS Headers** (4.7.0) - Permissão de requisições Cross-Origin
- **DJ Database URL** (2.3.0) - Configuração do banco via URL
- **WhiteNoise** (6.9.0) - Serviço de arquivos estáticos
- [Frontend do projeto](https://github.com/T-Terra/Frontend-estoque)

## 📌 Instalação

1. **Clone o repositório**
   ```sh
   git clone https://github.com/T-Terra/Backend-estoque.git
   cd Backend-estoque
   ```

2. **Crie e ative um ambiente virtual**
   ```sh
   poetry env use python # Caso utilize o poetry
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate  # Windows
   ```

3. **Instale as dependências**
   ```sh
   pip install poetry
   poetry install
   ```

4. **Configure o banco de dados**
   ```sh
   python manage.py migrate
   ```

5. **Crie um superusuário (opcional)**
   ```sh
   python manage.py createsuperuser
   ```

6. **Execute o servidor**
   ```sh
   poetry run python manage.py runserver
   ```

## 🔗 Endpoints da API

### 📌 Autenticação
| Método | Rota                  | Descrição |
|---------|-----------------------|-------------|
| POST    | `/api/login/`         | Login e gera token JWT |
| POST    | `/api/register/`      | Registra um novo usuário |
| POST    | `/api/logout/`        | Logout do usuário |
| POST    | `/api/refreshtoken/`  | Atualiza o token JWT |
| GET     | `/api/authcheck/`     | Verifica autenticação |

### 📌 Peças
| Método | Rota             | Descrição |
|---------|----------------|-------------|
| GET     | `/api/pecas/`   | Lista todas as peças |
| POST    | `/api/pecas/`   | Adiciona uma nova peça |
| GET     | `/api/pecas/{id}/` | Obtém detalhes de uma peça |
| PUT     | `/api/pecas/{id}/` | Atualiza uma peça |
| DELETE  | `/api/pecas/{id}/` | Remove uma peça |

## 🔐 Autenticação
A API utiliza JWT (JSON Web Token) armazenado em HTTPOnly Cookies para autenticação. Isso significa que o token não fica acessível no JavaScript, aumentando a segurança contra ataques XSS.

**Como funciona:**

- **No login**, o backend envia um cookie HTTPOnly contendo o token de acesso.

- Para acessar rotas protegidas, o navegador automaticamente anexa o cookie nas requisições.

- O **refresh token** também é armazenado em cookie e usado para obter um novo token de acesso sem precisar relogar.

- No **logout**, os cookies são apagados no servidor.


## 🚀 Deploy
Para rodar em produção, utilize o Gunicorn:
```sh
poetry run gunicorn core.wsgi:application --bind 0.0.0.0:8000
```

## 📝 Licença
Este projeto está sob a licença **MIT**. Veja o arquivo `LICENSE` para mais detalhes.

