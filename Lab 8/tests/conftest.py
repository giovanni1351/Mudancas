import os
import sys

# Adiciona Lab 8/ ao sys.path para que os serviços sejam importáveis como pacotes:
#   from servico_candidatura.models import ...
#   from servico_notificacao.services import ...
LAB8_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if LAB8_ROOT not in sys.path:
    sys.path.insert(0, LAB8_ROOT)
