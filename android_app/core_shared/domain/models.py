"""
Core Shared - Domain Models
Versão desacoplada, pura, sem dependência de UI.
Pode ser usada por Desktop, Kivy, Flutter (via API), etc.
"""
from dataclasses import dataclass, field
from typing import List, Optional, Set, Dict
from enum import Enum

class ModoTreino(str, Enum):
    HISTORICO = "Historico"
    CAOS = "Caos Aleatorio"

class EstrategiaPredefinida(str, Enum):
    CONSERVADOR = "Conservador"
    AGRESSIVO = "Agressivo"
    ROBO_PREGUICOSO = "Robo Preguicoso"  # Apriori + Auto + RL
    COFRE_SEGURO = "Cofre Seguro"

@dataclass
class Filtros:
    """Filtros de fechamento. None = desativado, int = valor exato alvo."""
    impar: Optional[int] = None
    moldura: Optional[int] = None
    primos: Optional[int] = None
    soma: Optional[int] = None
    sequencia_max: Optional[int] = None
    fibonacci: Optional[int] = None
    bloqueadas: List[int] = field(default_factory=list)
    fixas: List[int] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            "impar": self.impar,
            "moldura": self.moldura,
            "primos": self.primos,
            "soma": self.soma,
            "sequencia": self.sequencia_max,
            "fibonacci": self.fibonacci,
            "bloqueadas": self.bloqueadas,
            "fixas": self.fixas,
        }

    @classmethod
    def from_legacy(cls, legacy: dict) -> "Filtros":
        """Converte formato antigo (bool ou int) para novo."""
        def parse_val(v):
            if isinstance(v, bool):
                return None if not v else True  # True vira flag para usar padrão
            return v

        return cls(
            impar=legacy.get("impar") if isinstance(legacy.get("impar"), int) else None,
            moldura=legacy.get("moldura") if isinstance(legacy.get("moldura"), int) else None,
            primos=legacy.get("primos") if isinstance(legacy.get("primos"), int) else None,
            soma=legacy.get("soma") if isinstance(legacy.get("soma"), int) else None,
            sequencia_max=legacy.get("sequencia"),
            fibonacci=legacy.get("fibonacci"),
            bloqueadas=legacy.get("bloqueadas", []),
            fixas=[],
        )

@dataclass
class ConfigGeracao:
    """Configuração completa de uma execução do motor."""
    num_jogos: int = 15
    tam_base: int = 20
    tam_jogo: int = 15
    populacao: int = 30  # Mobile usa 30 vs 50 desktop para economizar bateria
    elite: int = 8
    taxa_mutacao: float = 0.05
    severidade: float = 0.8
    filtros: Filtros = field(default_factory=Filtros)
    foco_14: bool = False
    apriori_ativo: bool = False
    auto_piloto: bool = False
    modo_treino: ModoTreino = ModoTreino.HISTORICO
    memoria_ativa: bool = True
    hamming: bool = False
    max_geracoes: int = 100
    simulacoes_por_avaliacao: int = 1000  # Mobile 1000 vs 5000 desktop
    usar_turbo: bool = False  # Mobile desativa por padrão

@dataclass
class EstatisticasAcertos:
    h11: int = 0
    h12: int = 0
    h13: int = 0
    h14: int = 0
    h15: int = 0
    ruins: int = 0

    @property
    def total(self) -> int:
        return self.h11 + self.h12 + self.h13 + self.h14 + self.h15 + self.ruins

@dataclass
class ResultadoGeracao:
    """Resultado de UMA geração."""
    geracao: int
    base_20: List[int]
    sistema: List[List[int]]
    score: float
    stats: EstatisticasAcertos
    sharpe: float
    lucro_medio: float
    relaxou: bool
    tempo_ms: int

@dataclass
class MatrizSalva:
    """Para ranking Top 50."""
    id: str
    score: float
    base_20: List[int]
    sistema: List[List[int]]
    stats: EstatisticasAcertos
    geracao: int
    timestamp: str
    qtd_jogos: int
    favorita: bool = False

@dataclass
class Sorteio:
    concurso: int
    data: str
    dezenas: Set[int]

@dataclass
class AnaliseAtraso:
    dezena: int
    atual: int
    media: float
    limite: float
    status: str  # NORMAL, ESTOURANDO

@dataclass
class PrevisaoMarkov:
    dezena: int
    peso: float

@dataclass
class ResultadoInteligencia:
    top_5: List[int]
    ranking_completo: List[Dict]  # [{"dezena":1, "score": 85.2}, ...]
    relatorio: str
    tipo: str  # atrasometro, markov, ensemble, apriori
