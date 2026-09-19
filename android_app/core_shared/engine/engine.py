"""
Motor Lotofácil Lite - versão desacoplada sem Queue, sem UI, sem customtkinter.
Pode ser usado por desktop, Kivy, Flutter via API, testes.
"""
import random
import time
import gc
from typing import List, Set, Dict, Callable, Optional, Tuple
from collections import Counter
from .genetic_lite import gerar_sistema, crossover, mutacao, filtrar_diversidade
from .evaluator_lite import avaliar
from .fechamento import gerar_desdobramento
from ..domain.models import ConfigGeracao, ResultadoGeracao, EstatisticasAcertos
from ..data.repository import SorteioRepository
from ..utils.logger import logger

class MotorLotofacilLite:
    """
    Motor genético lite, com callbacks ao invés de Queue.
    """
    def __init__(
        self,
        repository: SorteioRepository,
        on_progress: Optional[Callable[[ResultadoGeracao], None]] = None,
        on_anomalia: Optional[Callable[[str], None]] = None,
        on_log: Optional[Callable[[str], None]] = None,
    ):
        self.repo = repository
        self.on_progress = on_progress
        self.on_anomalia = on_anomalia
        self.on_log = on_log

        self._rodando = False
        self._pausado = False
        self._geracao_atual = 0
        self._melhor_score = float('-inf')
        self._historico_scores: List[float] = []
        self._historico_media: List[float] = []

        # Cache sorteios
        self._sorteios_treino: List[Set[int]] = []
        self._combos_ouro: List[Set[int]] = []

    def _log(self, msg: str):
        if self.on_log:
            self.on_log(msg)
        logger.info(msg)

    def _anomalia(self, msg: str):
        if self.on_anomalia:
            self.on_anomalia(msg)
        logger.warning(msg)

    def carregar_sorteios(self):
        self._log("📥 Carregando sorteios...")
        self._sorteios_treino = self.repo.get_todos()
        if not self._sorteios_treino:
            self._anomalia("Sem sorteios, usando random mock")
            self._sorteios_treino = [set(random.sample(range(1, 26), 15)) for _ in range(1000)]
        self._log(f"✅ {len(self._sorteios_treino)} sorteios carregados")

    def parar(self):
        self._rodando = False
        self._log("⏹️ Motor parado")

    def pausar(self):
        self._pausado = not self._pausado
        self._log("⏸️ Pausado" if self._pausado else "▶️ Retomado")

    def gerar(
        self,
        config: ConfigGeracao,
        memoria_pesos: Optional[Dict[str, int]] = None,
        combos_ouro: Optional[List[Set[int]]] = None,
    ) -> List[ResultadoGeracao]:
        """
        Gera matrizes evoluindo por max_geracoes.
        Retorna lista de ResultadoGeracao (um por geração).
        """
        self._rodando = True
        self._geracao_atual = 0
        resultados: List[ResultadoGeracao] = []

        if not self._sorteios_treino:
            self.carregar_sorteios()

        # População inicial
        pop: List[Set[int]] = []
        # Tenta carregar de ranking anterior se houver memória
        for _ in range(config.populacao):
            pop.append(gerar_sistema(
                memoria_pesos=memoria_pesos,
                bloqueadas=config.filtros.bloqueadas,
                fixas=config.filtros.fixas,
                severidade=config.severidade,
                memoria_ativa=config.memoria_ativa,
                tam_base=config.tam_base,
            ))

        self._log(f"🚀 Motor iniciado: Pop={config.populacao}, Elite={config.elite}, Jogos={config.num_jogos}, Gerações={config.max_geracoes}")

        for g in range(config.max_geracoes):
            if not self._rodando:
                break

            while self._pausado and self._rodando:
                time.sleep(0.5)

            start_gen = time.time()

            # Avalia população
            avaliados = []
            for individuo in pop:
                score, h11, h12, h13, h14, h15, ruins, sistema, relaxou = avaliar(
                    individuo_20=individuo,
                    filtros=config.filtros.to_dict(),
                    num_jogos=config.num_jogos,
                    sorteios_treino=self._sorteios_treino,
                    modo_treino=config.modo_treino.value if hasattr(config.modo_treino, 'value') else str(config.modo_treino),
                    foco_14=config.foco_14,
                    combos_ouro=combos_ouro or self._combos_ouro,
                    simulacoes=config.simulacoes_por_avaliacao,
                    tam_jogo=config.tam_jogo,
                )
                avaliados.append((individuo, score, h11, h12, h13, h14, h15, ruins, sistema, relaxou))

            avaliados.sort(key=lambda x: x[1], reverse=True)
            melhor = avaliados[0]
            media_pop = sum(a[1] for a in avaliados) / len(avaliados)

            self._historico_scores.append(melhor[1])
            self._historico_media.append(media_pop)

            if melhor[1] > self._melhor_score:
                self._melhor_score = melhor[1]

            # Cria resultado
            stats = EstatisticasAcertos(h11=melhor[2], h12=melhor[3], h13=melhor[4], h14=melhor[5], h15=melhor[6], ruins=melhor[7])
            resultado = ResultadoGeracao(
                geracao=g,
                base_20=sorted(list(melhor[0])),
                sistema=melhor[8],
                score=melhor[1],
                stats=stats,
                sharpe=0.0,  # poderia calcular
                lucro_medio=melhor[1] / len(melhor[8]) if melhor[8] else 0,
                relaxou=melhor[9],
                tempo_ms=int((time.time() - start_gen) * 1000),
            )
            resultados.append(resultado)

            if self.on_progress:
                self.on_progress(resultado)

            if resultado.relaxou and g % 5 == 0:
                self._anomalia(f"G{g}: Filtros relaxados para encontrar jogos viáveis")

            if stats.h15 > 0:
                self._anomalia(f"🎉 JACKPOT G{g}: {stats.h15} prêmios 15pts!")

            # Evolução
            elite = [a[0] for a in avaliados[:config.elite]]
            nova_pop = elite.copy()

            tentativas = 0
            while len(nova_pop) < config.populacao and tentativas < 1000:
                pai, mae = random.sample(elite, 2) if len(elite) >= 2 else (elite[0], gerar_sistema(memoria_pesos, config.filtros.bloqueadas, config.filtros.fixas, config.severidade, config.memoria_ativa, config.tam_base))
                filho = crossover(pai, mae, config.filtros.bloqueadas, config.filtros.fixas, config.tam_base)
                filho = mutacao(filho, config.taxa_mutacao, config.filtros.bloqueadas, config.filtros.fixas, config.tam_base)
                if filtrar_diversidade(nova_pop, filho, usar_hamming=config.hamming, tam_base=config.tam_base):
                    nova_pop.append(filho)
                tentativas += 1

            while len(nova_pop) < config.populacao:
                nova_pop.append(gerar_sistema(memoria_pesos, config.filtros.bloqueadas, config.filtros.fixas, config.severidade, config.memoria_ativa, config.tam_base))

            pop = nova_pop
            self._geracao_atual = g

            if g % 10 == 0:
                gc.collect()

        self._rodando = False
        self._log(f"✅ Motor finalizado após {self._geracao_atual+1} gerações. Top: R$ {self._melhor_score:.2f}")
        return resultados

    def gerar_unica(
        self,
        config: ConfigGeracao,
        memoria_pesos: Optional[Dict[str, int]] = None,
    ) -> ResultadoGeracao:
        """
        Gera apenas uma matriz (sem evolução), útil para API rápida.
        """
        if not self._sorteios_treino:
            self.carregar_sorteios()

        individuo = gerar_sistema(
            memoria_pesos=memoria_pesos,
            bloqueadas=config.filtros.bloqueadas,
            fixas=config.filtros.fixas,
            severidade=config.severidade,
            memoria_ativa=config.memoria_ativa,
            tam_base=config.tam_base,
        )

        score, h11, h12, h13, h14, h15, ruins, sistema, relaxou = avaliar(
            individuo_20=individuo,
            filtros=config.filtros.to_dict(),
            num_jogos=config.num_jogos,
            sorteios_treino=self._sorteios_treino,
            modo_treino=config.modo_treino.value if hasattr(config.modo_treino, 'value') else str(config.modo_treino),
            foco_14=config.foco_14,
            simulacoes=config.simulacoes_por_avaliacao,
            tam_jogo=config.tam_jogo,
        )

        stats = EstatisticasAcertos(h11=h11, h12=h12, h13=h13, h14=h14, h15=h15, ruins=ruins)
        return ResultadoGeracao(
            geracao=0,
            base_20=sorted(list(individuo)),
            sistema=sistema,
            score=score,
            stats=stats,
            sharpe=0.0,
            lucro_medio=score / len(sistema) if sistema else 0,
            relaxou=relaxou,
            tempo_ms=0,
        )
