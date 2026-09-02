import requests
import json
import os

print("="*50)
print(" INICIANDO DOWNLOAD DA BASE DA LOTOFÁCIL ")
print("="*50)
print("Buscando todos os 3000+ resultados da Caixa Econômica...")

url = "https://loteriascaixa-api.herokuapp.com/api/lotofacil"

try:
    response = requests.get(url, timeout=15)
    
    if response.status_code == 200:
        dados = response.json()
        
        if not os.path.exists("storage"):
            os.makedirs("storage")
            
        caminho_arquivo = os.path.join("storage", "todos_resultados_caixa.json")
        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f)
            
        print(f"\n[SUCESSO] {len(dados)} sorteios foram gravados no seu arquivo de cache!")
        print(f"Caminho salvo: {caminho_arquivo}")
        print("\nVocê já pode abrir o seu Simulador Lotofácil Pro e iniciar a IA.")
    else:
        print(f"\n[ERRO] Falha ao baixar da API. Código de erro: {response.status_code}")
        
except Exception as e:
    print(f"\n[ERRO CRÍTICO] Falha na conexão com a API: {e}")

print("="*50)
input("Pressione ENTER para fechar...")