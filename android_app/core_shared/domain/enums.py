from enum import Enum

class ModoTreino(str, Enum):
    HISTORICO = "Historico"
    CAOS = "Caos Aleatorio"
    BOOTSTRAP = "Bootstrap"

class TipoFiltro(str, Enum):
    IMPAR = "impar"
    MOLDURA = "moldura"
    PRIMOS = "primos"
    SOMA = "soma"
    SEQUENCIA = "sequencia"
    FIBONACCI = "fibonacci"

class EstrategiaPredefinida(str, Enum):
    CONSERVADOR = "Conservador"
    AGRESSIVO = "Agressivo"
    ROBO_PREGUICOSO = "Robo Preguicoso"
    COFRE_SEGURO = "Cofre Seguro"
    INVESTIDOR = "Investidor"

class TipoInteligencia(str, Enum):
    ATRASOMETRO = "atrasometro"
    MARKOV = "markov"
    ENSEMBLE = "ensemble"
    APRIORI = "apriori"
    AUTOPILOTO = "autopiloto"
    RL = "rl"

class TierUsuario(str, Enum):
    FREE = "free"
    PREMIUM_MENSAL = "premium_mensal"
    PREMIUM_ANUAL = "premium_anual"
    PREMIUM_VITALICIO = "premium_vitalicio"

class StatusMatriz(str, Enum):
    GERANDO = "gerando"
    CONCLUIDA = "concluida"
    FAVORITA = "favorita"
    ARQUIVADA = "arquivada"
