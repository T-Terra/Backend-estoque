import os
from django.contrib.auth import get_user_model
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv(override=True)

# Certificar-se de que o Django está configurado corretamente
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Importar a configuração do Django (após setar o DJANGO_SETTINGS_MODULE)
import django
django.setup()

User = get_user_model()

# Obter as variáveis de ambiente
username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "admin")

# Criar o superuser se não existir
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email='', password=password)
    print(f"Superuser {username} criado com sucesso!")
else:
    print(f"Superuser {username} já existe.")