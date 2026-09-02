import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import threading
import json
import time
import os
import shutil

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from core.engine import MotorLotofacil
from core.learner import inicializar_memoria
from core.data import load, save

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class Aplicacao(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.memoria_ativa = ctk.BooleanVar(value=True)
        self.gestao_banca_ativa = ctk.BooleanVar(value=False)
        self.inteligencia_hibrida = ctk.BooleanVar(value=False)
        self.markov_ativa = ctk.BooleanVar(value=False)
        self.filtro_hamming = ctk.BooleanVar(value=False)
        self.ensemble_ativo = ctk.BooleanVar(value=False) 
        self.foco_14_pontos = ctk.BooleanVar(value=False) # NOVO: O botão Cofre Seguro
        self.tema_atual = ctk.StringVar(value="Dark")
        self.matriz_selecionada = None
        
        self.title("Simulador Lotofácil Pro - Cockpit Lab V11 (Estratégia Cofre Seguro)")
        self.geometry("1450x850")
        self.minsize(1200, 800)
        
        inicializar_memoria()
        self.criar_interface()
        self.atualizar_combo_ecossistemas()

        self.engine = MotorLotofacil()
        self.processar_esteira()

    def processar_esteira(self):
        self.engine.params = {
            "foco_14": self.foco_14_pontos.get(),
            "ensemble_ativo": self.ensemble_ativo.get(),
            "filtro_hamming": self.filtro_hamming.get(),
            "hibrida": self.inteligencia_hibrida.get(),
            "markov_ativa": self.markov_ativa.get(),
            "modo_treino": self.combo_modo_treino.get(),
            "semente_ativa": self.chk_semente.get() == 1,
            "qtd_jogos": self.entry_qtd_jogos.get(),
            "bloqueadas": self.entry_bloqueadas.get(),
            "fixas": self.entry_fixas.get(),
            "impar": self.chk_impar.get() == 1,
            "moldura": self.chk_moldura.get() == 1,
            "primos": self.chk_primos.get() == 1,
            "soma": self.chk_soma.get() == 1,
            "sequencia": self.chk_sequencia.get() == 1,
            "fibonacci": self.chk_fibonacci.get() == 1,
            "apriori_ativo": self.chk_apriori.get() == 1,
            "auto_piloto": self.chk_autopiloto.get() == 1,
            "rl_ativo": self.chk_rl.get() == 1,
            "taxa_mutacao": self.slider_mutacao.get(),
            "severidade": self.slider_severidade.get(),
            "memoria_ativa": self.memoria_ativa.get(),
            "gestao_banca_ativa": self.gestao_banca_ativa.get(),
            "banca": self.entry_banca.get()
        }

        while not self.engine.msg_queue.empty():
            msg = self.engine.msg_queue.get()
            tipo = msg["tipo"]
            conteudo = msg["conteudo"]
            
            if tipo == "log": self._update_log(conteudo)
            elif tipo == "anomalia": self._add_anomalia(conteudo)
            elif tipo == "update_stats": self._update_stats(msg["freq_dict"], msg["quentes"], msg["frias"])
            elif tipo == "update_grafico": self.atualizar_grafico_view()
            elif tipo == "update_ml_panel": self._update_ml_panel(conteudo)
            elif tipo == "set_fixas_ui": self._set_fixas_ui(conteudo)
            elif tipo == "update_detalhes": self._append_detalhes(conteudo)
            elif tipo == "refresh_ecos": self.atualizar_combo_ecossistemas()
            elif tipo == "update_sliders": 
                self.slider_mutacao.set(conteudo["taxa_mutacao"])
                self.slider_severidade.set(conteudo["severidade"])
                self.atualizar_labels_slider(None)

        self.after(100, self.processar_esteira)

    def mudar_tema(self, escolha):
        ctk.set_appearance_mode(escolha)
        self.atualizar_grafico_view()

    def _update_log(self, texto):
        self.log.insert(tk.END, texto)
        if int(float(self.log.index(tk.END))) > 500: self.log.delete("1.0", "2.0")
        self.log.see(tk.END)

    def _add_anomalia(self, texto):
        horario = time.strftime("%H:%M:%S")
        self.txt_anomalias.insert(tk.END, f"[{horario}] ⚠️ {texto}\n")
        self.txt_anomalias.see(tk.END)

    def _update_stats(self, freq_dict, quentes, frias):
        self.lbl_quentes_val.configure(text="\n".join([f"Dez {n:02d}" for n, qtd in quentes]))
        self.lbl_frias_val.configure(text="\n".join([f"Dez {n:02d}" for n, qtd in frias]))
        if freq_dict:
            max_freq = max(freq_dict.values()) if freq_dict else 1
            for n in range(1, 26):
                f = freq_dict.get(n, 0)
                ratio = f / max_freq if max_freq > 0 else 0
                color = ("#e0e0e0", "#333333") if ratio < 0.2 else "#17a2b8" if ratio < 0.4 else "#ffc107" if ratio < 0.6 else "#fd7e14" if ratio < 0.8 else "#dc3545"
                self.grid_heatmap[n].configure(fg_color=color)

    def _update_ml_panel(self, texto):
        self.txt_atrasometro.delete("1.0", tk.END)
        self.txt_atrasometro.insert(tk.END, texto)

    def _set_fixas_ui(self, texto):
        self.entry_fixas.delete(0, tk.END)
        self.entry_fixas.insert(0, texto)
        
    def _append_detalhes(self, txt):
        self.txt_detalhes.insert(tk.END, txt)
        self.txt_detalhes.see(tk.END)

    def atualizar_grafico_view(self):
        historico_scores = self.engine.historico_scores
        historico_media_pop = self.engine.historico_media_pop
        
        for widget in self.frame_grafico_container.winfo_children(): widget.destroy()
        if not historico_scores: return
        
        bg_color = '#ffffff' if self.tema_atual.get() == "Light" else '#1e1e1e'
        text_color = 'black' if self.tema_atual.get() == "Light" else 'white'
        
        fig = Figure(figsize=(8, 4), dpi=100)
        fig.patch.set_facecolor(bg_color)
        ax = fig.add_subplot(111)
        ax.set_facecolor(bg_color)
        ax.tick_params(colors=text_color)
        ax.spines['bottom'].set_color(text_color)
        ax.spines['left'].set_color(text_color)
        
        ax.plot(historico_scores, color="#28a745", label="Top 1")
        ax.plot(historico_media_pop, color="#17a2b8", label="Média (Saúde)")
        ax.axhline(0, color='#dc3545', linestyle='--')
        ax.legend()
        
        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafico_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def cmd_testar_historico(self):
        if self.matriz_selecionada:
            self._append_detalhes("\n⏳ Iniciando Prova de Fogo contra Histórico da Caixa...\n")
            self.engine.executar_stress_test(self.matriz_selecionada, "historico")
        else: self._add_anomalia("Selecione uma matriz no Ranking Top 50 primeiro!")

    def cmd_testar_caos(self):
        if self.matriz_selecionada:
            self._append_detalhes("\n🌀 Iniciando Prova de Fogo contra 100.000 Sorteios (Caos)...\n")
            self.engine.executar_stress_test(self.matriz_selecionada, "aleatorio")
        else: self._add_anomalia("Selecione uma matriz no Ranking Top 50 primeiro!")

    def cmd_testar_bootstrap(self):
        if self.matriz_selecionada:
            self._append_detalhes("\n📊 Iniciando Bootstrap Hipergeométrico (Reamostragem Científica)...\n")
            self.engine.executar_stress_test(self.matriz_selecionada, "bootstrap")
        else: self._add_anomalia("Selecione uma matriz no Ranking Top 50 primeiro!")

    def iniciar_thread(self):
        if not self.engine.rodando:
            self.engine.rodando = True
            self.engine.pausado = False
            self.tabview_principal.set("Painel de Voo")
            threading.Thread(target=self.engine.loop_genetico, daemon=True).start()

    def parar(self): self.engine.rodando = False
    
    def toggle_pausa(self):
        if self.engine.rodando:
            self.engine.pausado = not self.engine.pausado
            self._update_log(">>> PAUSADO <<<\n" if self.engine.pausado else ">>> RETOMADO <<<\n")

    def toggle_turbo(self):
        self.engine.turbo = not self.engine.turbo
        cor_on = ("#d97706", "#f59e0b") 
        cor_off = ("gray75", "gray25")
        self.btn_turbo.configure(fg_color=cor_on if self.engine.turbo else cor_off, text_color="white")

    def acionar_extincao(self):
        if messagebox.askyesno("Extinção", "Aniquilar 90% da população para quebrar o Ótimo Local?"):
            self.engine.evento_extincao = True

    def acionar_atrasometro_manual(self):
        threading.Thread(target=self.engine.acionar_atrasometro, daemon=True).start()

    def modo_estavel(self):
        self.slider_mutacao.set(2); self.slider_severidade.set(80); self.memoria_ativa.set(True)
        self.atualizar_labels_slider(None); self._add_anomalia("Modo Conservador Ativado.")

    def modo_agressivo(self):
        self.slider_mutacao.set(15); self.slider_severidade.set(10); self.memoria_ativa.set(False)
        self.atualizar_labels_slider(None); self._add_anomalia("Modo Exploratório (Caos) Ativado.")

    def criar_snapshot(self):
        if not os.path.exists("storage/snapshots"): os.makedirs("storage/snapshots")
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        qtd_str = self.entry_qtd_jogos.get().strip()
        eco = int(qtd_str) if qtd_str.isdigit() and int(qtd_str) > 0 else 33
        arquivo = f"storage/melhores_matriz_{eco}.json"
        if os.path.exists(arquivo):
            shutil.copy(arquivo, f"storage/snapshots/snap_eco{eco}_{timestamp}.json")
            self._add_anomalia(f"Máquina do Tempo: Snapshot Eco {eco} salvo.")

    def atualizar_labels_slider(self, val):
        self.lbl_mut_val.configure(text=f"{int(self.slider_mutacao.get())}%")
        self.lbl_sev_val.configure(text=f"{int(self.slider_severidade.get())}%")

    def atualizar_combo_ecossistemas(self):
        if not os.path.exists("storage"): os.makedirs("storage")
        arquivos = [f for f in os.listdir("storage") if f.startswith("melhores_matriz_") and f.endswith(".json")]
        ecossistemas = [arq.replace("melhores_matriz_", "").replace(".json", "") for arq in arquivos]
        ecos_validos = sorted([e for e in ecossistemas if e.isdigit()], key=int)
        if not ecos_validos: ecos_validos = ["33"]
        
        ecos_str = [str(e) for e in ecos_validos]
        atual_rank = self.combo_rank_eco.get()
        atual_top3 = self.combo_top3_eco.get()
        
        self.combo_rank_eco.configure(values=ecos_str)
        self.combo_top3_eco.configure(values=ecos_str)
        
        if atual_rank not in ecos_str: self.combo_rank_eco.set(ecos_str[-1]) 
        if atual_top3 not in ecos_str: self.combo_top3_eco.set(ecos_str[-1])

    def atualizar_ranking_view(self, ev=None):
        self.atualizar_combo_ecossistemas()
        eco = self.combo_rank_eco.get()
        base = load(f"melhores_matriz_{eco}.json")
        
        for widget in self.scroll_ranking.winfo_children(): widget.destroy()
        if not base: return ctk.CTkLabel(self.scroll_ranking, text=f"Nenhum dado no ecossistema de {eco} jogos.").pack(pady=20)
        
        for idx, item in enumerate(base):
            frm_item = ctk.CTkFrame(self.scroll_ranking, fg_color="transparent")
            frm_item.pack(fill="x", pady=2, padx=5)
            
            btn_detalhes = ctk.CTkButton(frm_item, text=f"Posição {idx+1:02d} | Saldo: R$ {item['score']:,.2f}", 
                                         font=("Consolas", 14), anchor="w", fg_color="transparent", text_color=("#005500", "#00ff00"), 
                                         command=lambda i=idx: self.abrir_detalhes_ranking(i))
            btn_detalhes.pack(side="left", fill="x", expand=True)
            
            btn_apagar = ctk.CTkButton(frm_item, text="❌", width=35, font=("Segoe UI", 12, "bold"), 
                                       fg_color="#dc3545", hover_color="#b02525", 
                                       command=lambda i=idx: self.remover_do_ranking(i))
            btn_apagar.pack(side="right", padx=(5, 0))

    def remover_do_ranking(self, index):
        eco = self.combo_rank_eco.get()
        arquivo = f"melhores_matriz_{eco}.json"
        base = load(arquivo)
        if 0 <= index < len(base):
            saldo_removido = base[index]['score']
            if messagebox.askyesno("Remoção Cirúrgica", f"Tem certeza que deseja apagar a Matriz da posição {index+1:02d} (R$ {saldo_removido:,.2f})?"):
                base.pop(index)
                save(arquivo, base)
                self._add_anomalia(f"✂️ Remoção Cirúrgica: Matriz de R$ {saldo_removido:,.2f} apagada do Eco {eco}.")
                self.txt_detalhes.delete("1.0", tk.END)
                self.matriz_selecionada = None
                self.atualizar_ranking_view()
                self.atualizar_top3_view()

    def abrir_detalhes_ranking(self, index):
        eco = self.combo_rank_eco.get()
        item = load(f"melhores_matriz_{eco}.json")[index]
        self.matriz_selecionada = item['sistema']
        self.txt_detalhes.delete("1.0", tk.END)
        self.txt_detalhes.insert(tk.END, f"📋 MATRIZ POS {index+1:02d} | ECOSSISTEMA: {eco} JOGOS | SALDO: R$ {item['score']:,.2f}\n")
        self.txt_detalhes.insert(tk.END, f"Acertos Médios: 11:[{item['stats'][0]}] | 12:[{item['stats'][1]}] | 13:[{item['stats'][2]}] | 14:[{item['stats'][3]}] | 15:[{item['stats'][4]}]\n\n")
        self.txt_detalhes.insert(tk.END, f"⭐ AS 20 DEZENAS DE OURO ⭐\n[ {' '.join([f'{n:02d}' for n in item['base_20']])} ]\n\n")
        qtd_jogos = len(item['sistema'])
        self.txt_detalhes.insert(tk.END, "-"*50 + f"\n REDE DE SINERGIA ({qtd_jogos} JOGOS MUTANTES) \n" + "-"*50 + "\n")
        for j, jogo in enumerate(item['sistema']): self.txt_detalhes.insert(tk.END, f"Aposta {j+1:02d}: [ {' '.join([f'{n:02d}' for n in sorted(jogo)])} ]\n")
        self.tabview_principal.set("Detalhes da Matriz")

    def atualizar_top3_view(self, ev=None):
        self.atualizar_combo_ecossistemas()
        eco = self.combo_top3_eco.get()
        base = load(f"melhores_matriz_{eco}.json")
        self.txt_top3.delete("1.0", tk.END)
        self.txt_top3.insert(tk.END, f"🏆 AS 3 MELHORES MATRIZES (ECOSSISTEMA {eco} JOGOS) 🏆\n\n")
        for i in range(min(3, len(base) if base else 0)):
            self.txt_top3.insert(tk.END, f"RANKING {i+1} - SALDO: R$ {base[i]['score']:.2f}\n")
            self.txt_top3.insert(tk.END, f"Base (20): [ {' '.join([f'{n:02d}' for n in base[i]['base_20']])} ]\n\n")

    def obter_texto_ajuda(self, topico):
        ajudas = {
            "intro": "👋 BEM-VINDO AO SIMULADOR LOTOFÁCIL PRO\n\nEste é um laboratório de Ciência de Dados focado em otimização genética e estatística avançada.\n\nUse o menu à esquerda para entender cada engrenagem do seu Cockpit antes de iniciar os motores.",
            "o_que_faz": "🤖 O QUE O PROGRAMA FAZ?\n\nO sistema utiliza um Algoritmo Genético e Machine Learning para analisar todo o histórico da Caixa. Ele gera populações de matrizes, testa contra resultados passados, cruza as melhores (Crossover) e aplica mutações.",
            "ler_log": "📊 COMO LER O LOG (RESULTADOS)\n\nCada linha mostra a evolução. \n• Top: O Lucro Médio Limpo.\n• Média: A média de todos os testes da IA. Deve ser sempre negativa (exploração).",
            "apostas": "🎲 COMO FUNCIONAM AS APOSTAS?\n\nA máquina faz um 'Desdobramento Mutante': fatia as 20 dezenas em X jogos de 15 números (padrão 33).",
            "regras_ouro": "⚖️ REGRAS DE OURO\n\nLoterias possuem alta variância estatística. Este software aumenta o Valor Esperado (EV), mas não prevê o futuro 100%.",
            "iniciar": "▶ INICIAR / PAUSAR\n\nAciona ou suspende o Algoritmo Genético.",
            "turbo": "🚀 MODO TURBO\n\nAtiva o Processamento Paralelo (Multicore).",
            "estavel": "🛠️ MODO ESTÁVEL\n\nComuta a IA para estado Conservador. Mutação cai e Severidade sobe.",
            "agressivo": "🔥 MODO AGRESSIVO\n\nComuta a IA para estado Exploratório (Caos).",
            "extincao": "☄️ EXTINÇÃO EM MASSA\n\nAciona um cataclismo genético, aniquilando 90% do DNA da população.",
            "snapshot": "📸 SNAPSHOT (BACKUP)\n\nExtrai um JSON com o DNA exato das matrizes.",
            "mutacao": "🎛️ TAXA DE MUTAÇÃO\n\nDefine a variância percentual (0-25%) dos genes.",
            "severidade": "⚙️ SEVERIDADE DA MEMÓRIA\n\nAplica penalidade às dezenas que resultam em ROI negativo.",
            "hibrida": "🧠 INTELIGÊNCIA HÍBRIDA\n\nAutomatiza a fixação de anomalias baseadas em atraso.",
            "jogos": "🎲 QTD DE JOGOS / MATRIZ ÍMÃ\n\nAltera o 'Ecossistema' em tempo real.",
            "banca": "🏦 GESTÃO DE BANCA\n\nEstabelece a barreira de capital para o Risco de Ruína."
        }
        return ajudas.get(topico, "Selecione um tópico à esquerda.")

    def mostrar_ajuda(self, topico):
        self.txt_ajuda_display.configure(state="normal")
        self.txt_ajuda_display.delete("1.0", tk.END)
        self.txt_ajuda_display.insert(tk.END, self.obter_texto_ajuda(topico))
        self.txt_ajuda_display.configure(state="disabled")

    def criar_interface(self):
        self.grid_columnconfigure(0, weight=4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.tabview_principal = ctk.CTkTabview(self, corner_radius=10)
        self.tabview_principal.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        
        t_guia = self.tabview_principal.add("📖 Guia Interativo")
        t_cockpit = self.tabview_principal.add("Painel de Voo")
        t_anomalias = self.tabview_principal.add("Caçador de Anomalias")
        t_grafico = self.tabview_principal.add("Convergência (ECG)")
        t_atraso = self.tabview_principal.add("Atrasômetro / IA")
        t_ranking = self.tabview_principal.add("Ranking Top 50")
        t_top3 = self.tabview_principal.add("Top 3")
        t_detalhes = self.tabview_principal.add("Detalhes da Matriz")
        
        self.txt_ajuda_display = ctk.CTkTextbox(t_guia, font=("Segoe UI", 16), text_color=("black", "white"), fg_color=("gray95", "gray12"), corner_radius=10)
        self.txt_ajuda_display.pack(fill="both", expand=True, padx=10, pady=10)

        # ABA COCKPIT
        frame_btns = ctk.CTkFrame(t_cockpit, fg_color="transparent")
        frame_btns.pack(fill="x", pady=5)
        btn_font = ("Segoe UI", 13, "bold")
        ctk.CTkButton(frame_btns, text="▶ Iniciar Motor", font=btn_font, fg_color="#28a745", command=self.iniciar_thread).pack(side="left", padx=5)
        ctk.CTkButton(frame_btns, text="⏸ Pausar", font=btn_font, fg_color="#ffc107", text_color="black", command=self.toggle_pausa).pack(side="left", padx=5)
        ctk.CTkButton(frame_btns, text="⏹ Parar", font=btn_font, fg_color="#dc3545", command=self.parar).pack(side="left", padx=5)
        self.btn_turbo = ctk.CTkButton(frame_btns, text="🚀 Turbo", font=btn_font, fg_color="gray25", text_color="white", command=self.toggle_turbo)
        self.btn_turbo.pack(side="left", padx=5)
        self.log = ctk.CTkTextbox(t_cockpit, font=("Consolas", 14), text_color="#00ff00", fg_color="gray12", corner_radius=8)
        self.log.pack(fill="both", expand=True, pady=5)

        self.txt_anomalias = ctk.CTkTextbox(t_anomalias, font=("Consolas", 14), text_color="#ffcc00", fg_color="gray12", corner_radius=8)
        self.txt_anomalias.pack(fill="both", expand=True, pady=10)
        
        self.frame_grafico_container = ctk.CTkFrame(t_grafico, fg_color="transparent")
        self.frame_grafico_container.pack(fill="both", expand=True, pady=10)
        ctk.CTkButton(t_grafico, text="Atualizar Gráfico", font=btn_font, command=self.atualizar_grafico_view).pack()

        # ABA ATRASOMETRO / IA 
        frm_botoes_ia = ctk.CTkFrame(t_atraso, fg_color="transparent")
        frm_botoes_ia.pack(pady=10)
        ctk.CTkButton(frm_botoes_ia, text="🔄 Heurística (Atrasos)", font=btn_font, fg_color="#6f42c1", command=lambda: threading.Thread(target=self.engine.acionar_atrasometro, daemon=True).start()).pack(side="left", padx=5)
        ctk.CTkButton(frm_botoes_ia, text="🔗 Markov (Preditiva)", font=btn_font, fg_color="#17a2b8", command=lambda: threading.Thread(target=self.engine.acionar_markov, daemon=True).start()).pack(side="left", padx=5)
        ctk.CTkButton(frm_botoes_ia, text="👑 Rodar Ensemble Híbrido (XGBoost)", font=btn_font, fg_color="#dc3545", command=lambda: threading.Thread(target=self.engine.acionar_ensemble, daemon=True).start()).pack(side="left", padx=5)
        self.txt_atrasometro = ctk.CTkTextbox(t_atraso, font=("Consolas", 14), fg_color="gray12", corner_radius=8)
        self.txt_atrasometro.pack(fill="both", expand=True, pady=10)

        # ABA RANKING / TOP 3
        frm_rank_top = ctk.CTkFrame(t_ranking, fg_color="transparent"); frm_rank_top.pack(fill="x", pady=5)
        self.combo_rank_eco = ctk.CTkOptionMenu(frm_rank_top, values=["33"], command=self.atualizar_ranking_view); self.combo_rank_eco.pack(side="left", padx=5)
        ctk.CTkButton(frm_rank_top, text="🔄 Atualizar Lista", font=btn_font, command=self.atualizar_ranking_view).pack(side="right", padx=10)
        self.scroll_ranking = ctk.CTkScrollableFrame(t_ranking, fg_color="gray12", corner_radius=8); self.scroll_ranking.pack(fill="both", expand=True, padx=10, pady=10)
        
        frm_top3_top = ctk.CTkFrame(t_top3, fg_color="transparent"); frm_top3_top.pack(fill="x", pady=5)
        self.combo_top3_eco = ctk.CTkOptionMenu(frm_top3_top, values=["33"], command=self.atualizar_top3_view); self.combo_top3_eco.pack(side="left", padx=5)
        ctk.CTkButton(frm_top3_top, text="🔄 Carregar Top 3", font=btn_font, command=self.atualizar_top3_view).pack(side="right", padx=10)
        self.txt_top3 = ctk.CTkTextbox(t_top3, font=("Consolas", 14), fg_color="gray12", corner_radius=8); self.txt_top3.pack(fill="both", expand=True, padx=10, pady=10)
        
        # ABA DETALHES E STRESS TEST
        frm_detalhes_top = ctk.CTkFrame(t_detalhes, fg_color="transparent"); frm_detalhes_top.pack(fill="x", pady=5)
        ctk.CTkButton(frm_detalhes_top, text="🧪 Stress: Histórico (Real)", font=btn_font, fg_color="#17a2b8", command=self.cmd_testar_historico).pack(side="left", padx=10)
        ctk.CTkButton(frm_detalhes_top, text="🌀 Stress: Caos 100k", font=btn_font, fg_color="#6f42c1", command=self.cmd_testar_caos).pack(side="left", padx=10)
        ctk.CTkButton(frm_detalhes_top, text="📊 Stress: Bootstrap Hipergeométrico", font=btn_font, fg_color="#d97706", command=self.cmd_testar_bootstrap).pack(side="left", padx=10)
        self.txt_detalhes = ctk.CTkTextbox(t_detalhes, font=("Consolas", 14), fg_color="gray12", corner_radius=8); self.txt_detalhes.pack(fill="both", expand=True, padx=10, pady=10)

        # ==========================================
        # PAINEL DIREITO (CONTROLES E SLIDERS)
        # ==========================================
        frame_dir = ctk.CTkScrollableFrame(self, fg_color=("gray90", "gray10"), width=340, corner_radius=10)
        frame_dir.grid(row=0, column=1, padx=(0, 15), pady=15, sticky="nsew")
        
        frm_header = ctk.CTkFrame(frame_dir, fg_color="transparent"); frm_header.pack(fill="x", pady=5)
        ctk.CTkLabel(frm_header, text="⚙️ Painel de Controle", font=("Segoe UI", 18, "bold")).pack(side="left")
        self.seletor_tema = ctk.CTkOptionMenu(frm_header, values=["Dark", "Light"], width=80, command=self.mudar_tema, variable=self.tema_atual); self.seletor_tema.pack(side="right")
        
        ctk.CTkFrame(frame_dir, height=2, fg_color=("gray80", "gray20")).pack(fill="x", pady=10)
        
        ctk.CTkLabel(frame_dir, text="Rigor Científico", font=("Segoe UI", 12, "bold"), text_color="#4dabf7").pack(pady=(10, 0))
        self.combo_modo_treino = ctk.CTkOptionMenu(frame_dir, values=["Histórico", "Caos Aleatório"], width=180); self.combo_modo_treino.pack(pady=5, padx=10)
        self.chk_semente = ctk.CTkCheckBox(frame_dir, text="Semente Determinística"); self.chk_semente.pack(anchor="w", padx=10, pady=5)
        
        ctk.CTkLabel(frame_dir, text="🎛️ Hiperparâmetros", font=("Segoe UI", 15, "bold")).pack(pady=(15, 5))
        
        ctk.CTkButton(frame_dir, text="🤖 Auto-Tuning (Optuna)", font=("Segoe UI", 13, "bold"), corner_radius=6, fg_color="#28a745", command=lambda: self.engine.acionar_optuna()).pack(pady=(0, 10), fill="x", padx=5)

        frm_mut = ctk.CTkFrame(frame_dir, fg_color="transparent"); frm_mut.pack(fill="x")
        ctk.CTkLabel(frm_mut, text="Taxa de Mutação").pack(side="left", padx=5)
        self.lbl_mut_val = ctk.CTkLabel(frm_mut, text="2%", font=("Segoe UI", 12, "bold")); self.lbl_mut_val.pack(side="right", padx=5)
        self.slider_mutacao = ctk.CTkSlider(frame_dir, from_=1, to=25, command=self.atualizar_labels_slider); self.slider_mutacao.set(2); self.slider_mutacao.pack(fill="x", padx=5, pady=(0, 10))

        frm_sev = ctk.CTkFrame(frame_dir, fg_color="transparent"); frm_sev.pack(fill="x")
        ctk.CTkLabel(frm_sev, text="Severidade da Mem.").pack(side="left", padx=5)
        self.lbl_sev_val = ctk.CTkLabel(frm_sev, text="80%", font=("Segoe UI", 12, "bold")); self.lbl_sev_val.pack(side="right", padx=5)
        self.slider_severidade = ctk.CTkSlider(frame_dir, from_=0, to=100, command=self.atualizar_labels_slider); self.slider_severidade.set(80); self.slider_severidade.pack(fill="x", padx=5, pady=(0, 10))
        
        ctk.CTkSwitch(frame_dir, text="Ativar Memória de Erro", variable=self.memoria_ativa, progress_color="#28a745").pack(anchor="w", padx=10, pady=5)
        ctk.CTkSwitch(frame_dir, text="🧠 Inteligência Híbrida", variable=self.inteligencia_hibrida, progress_color="#6f42c1").pack(anchor="w", padx=10, pady=5)
        ctk.CTkSwitch(frame_dir, text="🔗 Modo Markov (Preditivo)", variable=self.markov_ativa, progress_color="#17a2b8").pack(anchor="w", padx=10, pady=5)
        ctk.CTkSwitch(frame_dir, text="🧬 Filtro de Diversidade (Hamming)", variable=self.filtro_hamming, progress_color="#e6a600").pack(anchor="w", padx=10, pady=5)
        ctk.CTkSwitch(frame_dir, text="👑 Ensemble Híbrido (XGBoost)", variable=self.ensemble_ativo, progress_color="#dc3545").pack(anchor="w", padx=10, pady=5)
        
        # O NOVO SWITCH DO COFRE SEGURO
        ctk.CTkSwitch(frame_dir, text="🎯 Estratégia Cofre Seguro (Foco 14)", variable=self.foco_14_pontos, progress_color="#d97706").pack(anchor="w", padx=10, pady=5)
        
        self.chk_apriori = ctk.CTkSwitch(frame_dir, text="💎 Mineração Apriori (Combos de Ouro)", progress_color="#ffd700")
        self.chk_apriori.pack(anchor="w", padx=10, pady=5)
        
        self.chk_autopiloto = ctk.CTkSwitch(frame_dir, text="🎯 Auto-Piloto de Filtros (XGBoost)", progress_color="#17a2b8")
        self.chk_autopiloto.pack(anchor="w", padx=10, pady=5)
        
        self.chk_rl = ctk.CTkSwitch(frame_dir, text="🤖 IA Autônoma (Rede Neural Profunda)", progress_color="#8a2be2")
        self.chk_rl.pack(anchor="w", padx=10, pady=(5, 15))
        
        btn_action_font = ("Segoe UI", 13)
        ctk.CTkButton(frame_dir, text="🛠️ Modo Estável", corner_radius=6, command=self.modo_estavel).pack(pady=3, fill="x", padx=5)
        ctk.CTkButton(frame_dir, text="🔥 Modo Agressivo", corner_radius=6, fg_color="#dc3545", command=self.modo_agressivo).pack(pady=3, fill="x", padx=5)
        ctk.CTkButton(frame_dir, text="☄️ Extinção em Massa", corner_radius=6, fg_color="#6f42c1", command=self.acionar_extincao).pack(pady=3, fill="x", padx=5)
        ctk.CTkButton(frame_dir, text="📸 Snapshot (Backup)", corner_radius=6, fg_color="#17a2b8", command=self.criar_snapshot).pack(pady=3, fill="x", padx=5)
        
        ctk.CTkFrame(frame_dir, height=2, fg_color=("gray80", "gray20")).pack(fill="x", pady=15)

        ctk.CTkLabel(frame_dir, text="🧬 Engenharia de DNA", font=("Segoe UI", 15, "bold")).pack(pady=5)
        
        entry_config = {"corner_radius": 6, "fg_color": ("white", "gray15"), "border_color": ("gray70", "gray30")}
        self.entry_qtd_jogos = ctk.CTkEntry(frame_dir, placeholder_text="Qtd de Jogos (Padrão: 33)", **entry_config); self.entry_qtd_jogos.pack(fill="x", padx=5, pady=5)
        self.entry_fixas = ctk.CTkEntry(frame_dir, placeholder_text="Matriz Ímã (Fixas): 13, 24", **entry_config); self.entry_fixas.pack(fill="x", padx=5, pady=5)
        self.entry_bloqueadas = ctk.CTkEntry(frame_dir, placeholder_text="Lista Negra (Banidas): 2", **entry_config); self.entry_bloqueadas.pack(fill="x", padx=5, pady=5)
        
        self.chk_impar = ctk.CTkCheckBox(frame_dir, text="Ímpares (7 ou 8)"); self.chk_impar.pack(anchor="w", padx=10, pady=2)
        self.chk_moldura = ctk.CTkCheckBox(frame_dir, text="Moldura (9 a 11)"); self.chk_moldura.pack(anchor="w", padx=10, pady=2)
        self.chk_primos = ctk.CTkCheckBox(frame_dir, text="Primos (4 a 6)"); self.chk_primos.pack(anchor="w", padx=10, pady=2)
        self.chk_soma = ctk.CTkCheckBox(frame_dir, text="Soma (180 a 210)"); self.chk_soma.pack(anchor="w", padx=10, pady=2)
        self.chk_sequencia = ctk.CTkCheckBox(frame_dir, text="Sequências (Max 6)"); self.chk_sequencia.pack(anchor="w", padx=10, pady=2)
        self.chk_fibonacci = ctk.CTkCheckBox(frame_dir, text="Fibonacci (4 a 6)"); self.chk_fibonacci.pack(anchor="w", padx=10, pady=2)

        ctk.CTkSwitch(frame_dir, text="Gestão de Banca (Alerta)", variable=self.gestao_banca_ativa, progress_color="#ffc107").pack(anchor="w", padx=10, pady=(10,5))
        self.entry_banca = ctk.CTkEntry(frame_dir, placeholder_text="Banca R$ (Ex: 1000)", **entry_config); self.entry_banca.pack(fill="x", padx=5)

        ctk.CTkFrame(frame_dir, height=2, fg_color=("gray80", "gray20")).pack(fill="x", pady=15)
        ctk.CTkLabel(frame_dir, text="🔥 Heatmap Sensorial", font=("Segoe UI", 15, "bold")).pack(pady=5)
        
        frame_heatmap = ctk.CTkFrame(frame_dir, fg_color="transparent")
        frame_heatmap.pack(padx=5, pady=5)
        self.grid_heatmap = {}
        for i in range(25):
            n = i + 1
            lbl = ctk.CTkLabel(frame_heatmap, text=f"{n:02d}", width=32, height=32, corner_radius=6, font=("Segoe UI", 12, "bold"), fg_color=("gray80", "gray20"), text_color=("black", "white"))
            lbl.grid(row=i // 5, column=i % 5, padx=3, pady=3)
            self.grid_heatmap[n] = lbl

        self.lbl_quentes_val = ctk.CTkLabel(frame_dir, text="...", font=("Consolas", 12, "bold"), text_color="#ff6b6b"); self.lbl_quentes_val.pack(pady=2)
        self.lbl_frias_val = ctk.CTkLabel(frame_dir, text="...", font=("Consolas", 12, "bold"), text_color="#4dabf7"); self.lbl_frias_val.pack(pady=2)

def criar_interface():
    app = Aplicacao()
    app.mainloop()