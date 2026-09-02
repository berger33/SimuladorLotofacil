import logging
from logging.handlers import RotatingFileHandler
import os

# Garante que a pasta existe
os.makedirs("storage/logs", exist_ok=True)

# Configura o Logger Padrão Ouro da Indústria
logger = logging.getLogger("CockpitLotofacil")
logger.setLevel(logging.DEBUG) # Captura tudo (Info, Aviso, Erro)

# Evita que o log adicione a mesma mensagem duplicada se for recarregado
if not logger.handlers:
    # Cria um arquivo de log que chega até 5MB e guarda as últimas 3 versões
    file_handler = RotatingFileHandler(
        "storage/logs/system.log", maxBytes=5*1024*1024, backupCount=3, encoding="utf-8"
    )
    
    # Formato: [DATA/HORA] - [TIPO] - [MENSAGEM]
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)