import time
import gc
import random
import threading
import concurrent.futures
from collections import Counter
from queue import Queue
import math

from core.genetic import gerar_sistema, crossover, mutacao, filtrar_diversidade
from core.evaluator import avaliar, _carregar_bases_seguras
from core.learner import atualizar_memoria, penalizar_jogo
from core.data import load, save
from core.ml_intelligence import analisar_atrasos, gerar_previsao_markov, executar_ensemble_hibrido, minerar_regras_associacao, prever_macro_propriedades
from core.rl_agent import RLAgent
from core.logger import logger
from config import POPULACAO, ELITE, PREMIO_11, PREMIO_12, PREMIO_13, PREMIO_14, PREMIO_15, CUSTO_APOSTA

class MotorLotofacil:
    def __init__(self):
        self.rodando = False
        self.pausado = False
        self.turbo = False
        self.evento_extincao = False
        self.num_jogos_ativo = 33
        self.historico_scores = []
        self.historico_media_pop = []
        self.historico_h14 = []
        self.historico_h15 = []
        self.current_drawdown = 0.0
        
        self.msg_queue = Queue() 
        self.params = {}         
        self.rl_agent = RLAgent()
        self.estado_anterior_rl = "estagnado"
        self.acao_idx_anterior_rl = 0

    def send_msg(self, tipo, conteudo=None, **kwargs):
        mensagem = {"tipo": tipo, "conteudo": conteudo}
        mensagem.update(kwargs)
        self.msg_queue.put(mensagem)

    def acionar_optuna(self):
        threading.Thread(target=self._worker_optuna, daemon=True).start()

    def _worker_optuna(self):
        self.send_msg("log", "\n>>> 🤖 INICIANDO AUTO-TUNING (OPTUNA) <<<\nA IA está a calibrar os hiperparâmetros ótimos. Aguarde...\n")
        try:
            import optuna
            optuna.logging.set_verbosity(optuna.logging.WARNING)

            def objective(trial):
                mut = trial.suggest_int("taxa_mutacao", 1, 25)
                sev = trial.suggest_int("severidade", 0, 100)
                pop = [gerar_sistema([], [], sev / 100.0, True, 33) for _ in range(5)]
                filtros = {"impar": False, "moldura": False, "primos": False, "bloqueadas": []}
                # Passa o 'foco_14' como False e 'combos_ouro' vazio para o teste rápido do Optuna
                args_list = [(s, filtros, 33, "Histórico", False, False, []) for s in pop]
                resultados = [avaliar(a)[0] for a in args_list] 
                return sum(resultados) / len(resultados)

            study = optuna.create_study(direction="maximize")
            study.optimize(objective, n_trials=10) 
            best = study.best_params
            self.send_msg("update_sliders", best)
            self.send_msg("log", f"✅ Optuna Finalizado! Taxa Mutação ajustada para: {best['taxa_mutacao']}%, Severidade: {best['severidade']}%\n")
            self.send_msg("anomalia", f"Auto-Tuning Optuna ativado: Mut={best['taxa_mutacao']}% | Sev={best['severidade']}%")
        except ImportError:
            self.send_msg("anomalia", "⚠️ Optuna não instalado. No terminal execute: pip install optuna")
        except Exception as e:
            self.send_msg("anomalia", f"Erro no Optuna: {e}")

    def acionar_atrasometro(self):
        logger.info("Iniciando varredura de Machine Learning (Atrasômetro)")
        self.send_msg("log", "\n>>> EXECUTANDO MACHINE LEARNING (DESVIO PADRÃO) <<<\n")
        dados_atraso, anomalias = analisar_atrasos()
        texto_ml = "📊 ESTATÍSTICA DE ATRASOS (Base Real DEDUPLICADA)\n\n"
        for n, d in dados_atraso.items():
            texto_ml += f"Dezena {n:02d} | Atual: {d['atual']:02d} | Média Hist: {d['media']:.1f} | Ruptura: {d['limite']:.1f} | {d['status']}\n"
        if anomalias:
            self.send_msg("anomalia", f"Dezenas prestes a estourar: {anomalias}")
            texto_ml += f"\n🚨 ANOMALIAS DETECTADAS: {anomalias}\n"
            if self.params.get("hibrida"):
                self.send_msg("set_fixas_ui", ",".join(map(str, anomalias)))
                self.send_msg("log", f"🧠 Inteligência Híbrida Ativa: Dezenas {anomalias} fixadas!\n")
        self.send_msg("update_ml_panel", texto_ml)

    def acionar_markov(self):
        self.send_msg("log", "\n>>> EXECUTANDO IA: CADEIAS DE MARKOV (PROBABILIDADE CONDICIONAL) <<<\n")
        top_previsoes, probabilidades = gerar_previsao_markov()
        if not top_previsoes: return
        texto_mk = "🔗 REDE DE MARKOV (Top Probabilidades de Transição para o Próximo Sorteio)\n\n"
        for dezena, prob in probabilidades[:15]: 
            texto_mk += f"Dezena {dezena:02d} | Peso Condicional: {prob:.4f}\n"
        self.send_msg("update_ml_panel", texto_mk)
        self.send_msg("anomalia", f"Cadeias de Markov preveem forte sinergia para: {top_previsoes}")
        if self.params.get("markov_ativa"):
            self.send_msg("set_fixas_ui", ",".join(map(str, top_previsoes)))
            self.send_msg("log", f"🔗 IA Markov Ativa: Dezenas {top_previsoes} fixadas!\n")

    def acionar_ensemble(self):
        self.send_msg("log", "\n>>> EXECUTANDO O CONSELHO JEDI: ENSEMBLE HÍBRIDO <<<\n")
        top_5, relatorio = executar_ensemble_hibrido()
        self.send_msg("update_ml_panel", relatorio)
        self.send_msg("anomalia", f"Ensemble elegeu as dezenas definitivas: {top_5}")
        if self.params.get("ensemble_ativo"):
            self.send_msg("set_fixas_ui", ",".join(map(str, top_5)))
            self.send_msg("log", f"👑 Ensemble Ativo: Dezenas {top_5} injetadas na Matriz Ímã!\n")

    def salvar_melhor(self, m, num_jogos):
        arquivo = f"melhores_matriz_{num_jogos}.json"
        base = load(arquivo)
        base.append({"score": m[1], "base_20": sorted(list(m[0])), "stats": m[2:7], "sistema": [list(j) for j in m[8]]})
        save(arquivo, sorted(base, key=lambda x: x["score"], reverse=True)[:50])

    def executar_stress_test(self, sistema_jogos, tipo="historico"):
        self.send_msg("log", f"\n>>> INICIANDO PROVA DE FOGO ({tipo.upper()}) <<<\n")
        threading.Thread(target=self._worker_stress_test, args=(sistema_jogos, tipo), daemon=True).start()

    def _worker_stress_test(self, sistema_jogos, tipo):
        h11 = h12 = h13 = h14 = h15 = ruins = 0
        try:
            treino, validacao = _carregar_bases_seguras()
            base_real = treino + validacao
            
            if tipo == "historico":
                sorteios = base_real
                if not sorteios: return
                qtd_testes = len(sorteios)
            elif tipo == "bootstrap":
                qtd_testes = 20000
                sorteios = [random.choice(base_real) for _ in range(qtd_testes)]
            else: 
                qtd_testes = 100000
                sorteios = [set(random.sample(range(1, 26), 15)) for _ in range(qtd_testes)]
                
            custo_total = qtd_testes * len(sistema_jogos) * CUSTO_APOSTA
            
            for sorteio in sorteios:
                for jogo in sistema_jogos:
                    acertos = len(set(jogo) & sorteio)
                    if acertos == 15: h15 += 1
                    elif acertos == 14: h14 += 1
                    elif acertos == 13: h13 += 1
                    elif acertos == 12: h12 += 1
                    elif acertos == 11: h11 += 1
                    else: ruins += 1
            
            faturamento = (h11 * PREMIO_11) + (h12 * PREMIO_12) + (h13 * PREMIO_13) + (h14 * PREMIO_14) + (h15 * PREMIO_15)
            lucro = faturamento - custo_total
            roi_percent = (lucro / custo_total) * 100 if custo_total > 0 else 0
            
            relatorio = (
                f"\n\n{'='*50}\n🚀 RESULTADO DA PROVA DE FOGO: {tipo.upper()} 🚀\n{'='*50}\n"
                f"Sorteios: {qtd_testes:,}\nLucro Líquido: R$ {lucro:,.2f}\n"
                f"Rentabilidade (ROI): {roi_percent:.2f}%\n\n"
                f"15 Pontos: {h15:,} | 14 Pontos: {h14:,} | Bilhetes Perdidos: {ruins:,}\n"
            )
            
            if tipo == "bootstrap":
                prob_teorica_15 = 1 / 3268760.0
                esperado_15 = (qtd_testes * len(sistema_jogos)) * prob_teorica_15
                relatorio += f"\n🔬 Validação Hipergeométrica (Esperado 15 pts): {esperado_15:.4f}\n"
                relatorio += f"📈 Performance vs Teoria: {'Acima da Média' if h15 > esperado_15 else 'Dentro do Padrão'}\n"
                
            relatorio += f"{'='*50}\n"
            
            self.send_msg("update_detalhes", relatorio)
            self.send_msg("anomalia", f"Prova de Fogo ({tipo}) finalizada!")
        except Exception as e:
            logger.error(f"Erro no Stress Test: {e}")

    def loop_genetico(self):
        self.send_msg("log", ">>> SISTEMA IGNIPÇÃO: MOTOR HÍBRIDO INICIADO <<<\n")
        
        if self.params.get("hibrida"): self.acionar_atrasometro()
        if self.params.get("markov_ativa"): self.acionar_markov()
        if self.params.get("ensemble_ativo"): self.acionar_ensemble()

        qtd_jogos_str = str(self.params.get("qtd_jogos", "33")).strip()
        self.num_jogos_ativo = int(qtd_jogos_str) if qtd_jogos_str.isdigit() and int(qtd_jogos_str) > 0 else 33
        
        base_salva = load(f"melhores_matriz_{self.num_jogos_ativo}.json")
        pop = [set(item["base_20"]) for item in base_salva[:POPULACAO]] if base_salva else []
        g = 0
        executor = concurrent.futures.ProcessPoolExecutor()
        
        try:
            combos_ouro = []
            while self.rodando:
                while self.pausado and self.rodando: time.sleep(0.5)
                if not self.rodando: break

                qtd_jogos_str = str(self.params.get("qtd_jogos", "33")).strip()
                novo_num = int(qtd_jogos_str) if qtd_jogos_str.isdigit() and int(qtd_jogos_str) > 0 else 33
                
                if novo_num != self.num_jogos_ativo:
                    self.send_msg("log", f"\n>>> TRANSIÇÃO QUÂNTICA: MUDANDO DE {self.num_jogos_ativo} PARA {novo_num} JOGOS <<<\n")
                    self.num_jogos_ativo = novo_num
                    base_salva = load(f"melhores_matriz_{self.num_jogos_ativo}.json")
                    pop = [set(item["base_20"]) for item in base_salva[:POPULACAO]] if base_salva else []
                    self.historico_scores.clear(); self.historico_media_pop.clear()
                    self.historico_h14.clear(); self.historico_h15.clear()
                    self.send_msg("update_grafico"); self.send_msg("refresh_ecos")
                    g = 0 

                bloq_str = str(self.params.get("bloqueadas", ""))
                fixas_str = str(self.params.get("fixas", ""))
                bloqueadas = [int(x.strip()) for x in bloq_str.split(',') if x.strip().isdigit() and 1 <= int(x.strip()) <= 25]
                fixas = [int(x.strip()) for x in fixas_str.split(',') if x.strip().isdigit() and 1 <= int(x.strip()) <= 25]
                
                filtros_ativos = {
                    "impar": self.params.get("impar", False), 
                    "moldura": self.params.get("moldura", False), 
                    "primos": self.params.get("primos", False),
                    "soma": self.params.get("soma", False),
                    "sequencia": self.params.get("sequencia", False),
                    "fibonacci": self.params.get("fibonacci", False),
                    "bloqueadas": bloqueadas
                }
                
                rl_ativo = self.params.get("rl_ativo", False)
                if rl_ativo:
                    estado_atual = self.rl_agent.determinar_estado(self.historico_media_pop, self.historico_h14, self.historico_h15, self.current_drawdown)
                    if len(self.historico_media_pop) > 0:
                        recompensa = self.historico_media_pop[-1]
                        self.rl_agent.aprender(self.estado_anterior_rl, self.acao_idx_anterior_rl, recompensa, estado_atual)
                    
                    acao = self.rl_agent.escolher_acao(estado_atual)
                    self.estado_anterior_rl = estado_atual
                    self.acao_idx_anterior_rl = self.rl_agent.acao_atual_idx
                    
                    taxa_mutacao = acao["taxa_mutacao"] / 100.0
                    severidade = acao["severidade"] / 100.0
                    apriori_ativo = acao["apriori_ativo"]
                    auto_piloto = acao["auto_piloto"]
                    
                    if g % 10 == 0:
                        self.send_msg("log", f"🤖 [RL Agent] Estado: {estado_atual.upper()} | Estratégia Aplicada: {acao['nome']}\n")
                else:
                    auto_piloto = self.params.get("auto_piloto", False)
                    apriori_ativo = self.params.get("apriori_ativo", False)
                    taxa_mutacao, severidade = self.params.get("taxa_mutacao", 2) / 100.0, self.params.get("severidade", 80) / 100.0

                if auto_piloto:
                    if not hasattr(self, 'ultimas_previsoes_macro') or self.ultimas_previsoes_macro is None:
                        self.send_msg("log", "🎯 Auto-Piloto (XGBoost): Prevendo alvos exatos dos filtros para o próximo sorteio...\n")
                        self.ultimas_previsoes_macro = prever_macro_propriedades()
                        self.send_msg("log", f"🎯 Alvos do Auto-Piloto travados: {self.ultimas_previsoes_macro}\n")
                    filtros_ativos.update(self.ultimas_previsoes_macro)
                else:
                    self.ultimas_previsoes_macro = None
                    
                mem_ativa, usar_hamming = self.params.get("memoria_ativa", True), self.params.get("filtro_hamming", False)
                
                # Resgata o novo botão 'Estratégia Cofre Seguro'
                foco_14 = self.params.get("foco_14", False)
                apriori_ativo = self.params.get("apriori_ativo", False)
                
                if apriori_ativo and not combos_ouro:
                    self.send_msg("log", "💎 Mineração Apriori: Mapeando os Combos de Ouro do Histórico...\n")
                    combos_ouro = minerar_regras_associacao(top_n=15, tamanho_combo=3)
                    self.send_msg("log", f"💎 {len(combos_ouro)} Combos de Ouro (Trincas) descobertos! Bônus genético ativado.\n")
                elif not apriori_ativo:
                    combos_ouro = []

                while len(pop) < POPULACAO:
                    pop.append(gerar_sistema(bloqueadas, fixas, severidade, mem_ativa, self.num_jogos_ativo))

                modo_treino, semente_ativa = self.params.get("modo_treino", "Histórico"), self.params.get("semente_ativa", False)
                pop_com_filtros = [(s, filtros_ativos, self.num_jogos_ativo, modo_treino, semente_ativa, foco_14, combos_ouro) for s in pop]
                resultados = list(executor.map(avaliar, pop_com_filtros)) if self.turbo else [avaliar(args) for args in pop_com_filtros]

                avaliados = [(s, *res) for s, res in zip(pop, resultados)]
                avaliados.sort(key=lambda x: x[1], reverse=True)
                
                melhor, pior, media_pop = avaliados[0], avaliados[-1], sum(a[1] for a in avaliados) / len(avaliados)
                
                if melhor[9] and g % 10 == 0:
                    self.send_msg("anomalia", "Filtros muito restritos. O sistema precisou aplicar um relaxamento nas cartelas.")
                
                if self.params.get("gestao_banca_ativa"):
                    banca_str = str(self.params.get("banca", "1000"))
                    banca_atual = float(banca_str) if banca_str.replace('.', '', 1).isdigit() else 1000.0
                    self.current_drawdown = abs(pior[1]) if pior[1] < 0 else 0
                    if self.current_drawdown > banca_atual * 0.5: 
                        self.send_msg("anomalia", f"Risco de Ruína (Drawdown R${self.current_drawdown:.2f}) na Geração {g}")
                else:
                    self.current_drawdown = abs(pior[1]) if pior[1] < 0 else 0

                atualizar_memoria(melhor[0], mem_ativa)
                if pior[1] < 0: penalizar_jogo(pior[0], mem_ativa)

                self.historico_scores.append(melhor[1])
                self.historico_media_pop.append(media_pop)
                self.historico_h14.append(sum(a[5] for a in avaliados))
                self.historico_h15.append(sum(a[6] for a in avaliados))
                if len(self.historico_scores) > 100: 
                    self.historico_scores.pop(0); self.historico_media_pop.pop(0)
                    self.historico_h14.pop(0); self.historico_h15.pop(0)
                
                self.send_msg("update_grafico")

                lucro_ap = melhor[1] / len(melhor[8]) if len(melhor[8]) > 0 else 0
                status = f"G{g} (Eco: {self.num_jogos_ativo}) | Top: R$ {melhor[1]:.2f} (R$ {lucro_ap:.2f}/ap) | Média: R$ {media_pop:.2f} | 11a15:[{melhor[2]}/{melhor[3]}/{melhor[4]}/{melhor[5]}/{melhor[6]}]\n"
                self.send_msg("log", status)
                
                if melhor[6] > 0: self.send_msg("anomalia", f"JACKPOT! {melhor[6]} prêmios de 15 pts na G{g}")

                freq = Counter(melhor[0])
                dezenas_ordenadas = freq.most_common()
                self.send_msg("update_stats", freq_dict=dict(freq), quentes=dezenas_ordenadas[:5], frias=list(reversed(dezenas_ordenadas[-5:])))
                self.salvar_melhor(melhor, self.num_jogos_ativo)

                elite = [a[0] for a in avaliados[:ELITE]]
                nova = elite.copy()

                if self.evento_extincao:
                    self.send_msg("log", "\n>>> METEORO LANÇADO: EXTINÇÃO EM MASSA EXECUTADA <<<\n")
                    self.send_msg("anomalia", "Extinção em Massa provocou reset populacional.")
                    nova, self.evento_extincao = elite[:2], False

                tentativas_div = 0
                while len(nova) < POPULACAO and tentativas_div < 1000:
                    pai, mae = random.sample(elite, 2) if len(elite) >= 2 else (elite[0], gerar_sistema(bloqueadas, fixas, severidade, mem_ativa, self.num_jogos_ativo))
                    filho = mutacao(crossover(pai, mae, bloqueadas, fixas), taxa_mutacao, bloqueadas, fixas)
                    if filtrar_diversidade(nova, filho, usar_hamming=usar_hamming): nova.append(filho)
                    tentativas_div += 1

                while len(nova) < POPULACAO: nova.append(gerar_sistema(bloqueadas, fixas, severidade, mem_ativa, self.num_jogos_ativo))

                pop = nova
                g += 1
                if g % 10 == 0: gc.collect()

        except Exception as e:
            self.send_msg("anomalia", f"ERRO FATAL: {e}. Verifique o log.")
        finally:
            executor.shutdown(wait=False)