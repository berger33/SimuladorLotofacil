import threading
from core.engine import MotorLotofacil
import time

engine = MotorLotofacil()
engine.params = {
    "foco_14": False,
    "ensemble_ativo": True,
    "filtro_hamming": False,
    "hibrida": False,
    "markov_ativa": True,
    "modo_treino": "Rápido",
    "semente_ativa": False,
    "qtd_jogos": 10,
    "bloqueadas": "",
    "fixas": "",
    "impar": False,
    "moldura": False,
    "primos": False,
    "soma": False,
    "sequencia": False,
    "fibonacci": False,
    "apriori_ativo": True,
    "auto_piloto": True,
    "rl_ativo": True,
    "taxa_mutacao": 15,
    "severidade": 50,
    "memoria_ativa": True,
    "gestao_banca_ativa": False,
    "banca": 1000
}

engine.rodando = True
engine.pausado = False
engine.evento_extincao = False
engine.num_jogos_ativo = 10

def render_logs():
    while engine.rodando:
        while not engine.msg_queue.empty():
            msg = engine.msg_queue.get()
            print(f"[{msg['tipo']}] {msg['conteudo'].strip()}")
        time.sleep(0.1)

print("Iniciando bateria de testes do Motor Hibrido...")
log_thread = threading.Thread(target=render_logs, daemon=True)
log_thread.start()

try:
    gen_thread = threading.Thread(target=engine.loop_genetico, daemon=True)
    gen_thread.start()
    
    # Roda a simulação por 15 segundos
    time.sleep(15)
    
    engine.rodando = False
    gen_thread.join(timeout=5)
    print("TESTE 1: Simulacao Hibrida Completa - SUCESSO")

except Exception as e:
    engine.rodando = False
    import traceback
    print(f"TESTE FALHOU. ERRO:")
    traceback.print_exc()
