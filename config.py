NUM_JOGOS = 33   
TAM_BASE = 20    # A IA agora vai focar em escolher as 20 melhores dezenas
TAM_JOGO = 15    # O Fechamento fatiará as 20 em cartelas de 15
SIMULACOES = 5000

POPULACAO = 50   
ELITE = 10       

CUSTO_APOSTA = 3.00
PREMIO_11 = 6.00
PREMIO_12 = 12.00
PREMIO_13 = 30.00
PREMIO_14 = 2000.00     
PREMIO_15 = 600000.00

SOMA_MIN = 180
SOMA_MAX = 220
PRIMOS_ALVO = [5, 6]
PARES_ALVO = [7, 8]
MAX_SEQUENCIA = 4

# === REDE NEURAL LSTM ===
LSTM_TIME_STEPS = 15  # Quantos sorteios passados ela olha para prever o próximo
LSTM_EPOCHS = 30      # Quantas vezes ela vai treinar em cima dos dados