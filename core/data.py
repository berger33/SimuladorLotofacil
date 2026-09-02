import json
import os
import tempfile
import shutil

def load(filename: str) -> list:
    path = os.path.join("storage", filename)
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return []

def save(filename: str, data: list):
    os.makedirs("storage", exist_ok=True)
    path = os.path.join("storage", filename)
    
    # ESCRITA ATÔMICA: Cria um arquivo temporário invisível primeiro
    fd, temp_path = tempfile.mkstemp(dir="storage", text=True)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f)
            
        # Troca o arquivo temporário pelo oficial em 1 milissegundo (Safe-write)
        shutil.move(temp_path, path)
    except Exception as e:
        # Se algo der errado, apaga o temporário e protege o arquivo oficial antigo
        os.remove(temp_path)
        print(f"Erro crítico ao salvar dados: {e}")