"""
KivyMD MVP - Lotofácil Pro App
MVP rápido para validar mercado em 1 semana.
Reaproveita core_shared e gera APK via Buildozer.

Para rodar desktop:
  pip install kivy kivymd
  python main.py

Para gerar APK (Linux/WSL):
  buildozer android debug
"""
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import StringProperty, ListProperty, NumericProperty, BooleanProperty
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivy.uix.scrollview import ScrollView
import threading
import random
import time
import sys
import os

# Adiciona core_shared ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
try:
    from core_shared.domain.models import ConfigGeracao, Filtros, ModoTreino
    from core_shared.engine.genetic_lite import gerar_sistema, crossover, mutacao, filtrar_diversidade
    from core_shared.data.repository import LocalJsonRepository, CachedRepository, RemoteApiRepository
    CORE_AVAILABLE = True
except ImportError:
    CORE_AVAILABLE = False
    print("core_shared não encontrado, usando mock")

KV = '''
MDScreen:
    MDBoxLayout:
        orientation: 'vertical'
        
        MDTopAppBar:
            title: "Lotofácil Pro - MVP"
            left_action_items: [["menu", lambda x: None]]
            right_action_items: [["cog", lambda x: app.show_config()]]
            elevation: 2
        
        MDBottomNavigation:
            id: bottom_nav
            
            MDBottomNavigationItem:
                name: 'dashboard'
                text: 'Dashboard'
                icon: 'view-dashboard'
                
                ScrollView:
                    MDBoxLayout:
                        orientation: 'vertical'
                        adaptive_height: True
                        padding: dp(16)
                        spacing: dp(16)
                        
                        MDCard:
                            size_hint_y: None
                            height: dp(120)
                            padding: dp(16)
                            md_bg_color: 0.42, 0.26, 0.76, 1
                            radius: [16,]
                            MDBoxLayout:
                                orientation: 'vertical'
                                MDLabel:
                                    text: "Top Score"
                                    theme_text_color: "Custom"
                                    text_color: 1,1,1,1
                                    font_style: "H6"
                                MDLabel:
                                    id: lbl_top_score
                                    text: "R$ 0,00"
                                    theme_text_color: "Custom"
                                    text_color: 1,1,1,1
                                    font_style: "H4"
                                    bold: True
                                MDLabel:
                                    id: lbl_geracao
                                    text: "Geração: 0"
                                    theme_text_color: "Custom"
                                    text_color: 1,1,1,0.8
                        
                        MDCard:
                            size_hint_y: None
                            height: dp(200)
                            padding: dp(16)
                            radius: [16,]
                            MDBoxLayout:
                                orientation: 'vertical'
                                MDLabel:
                                    text: "📊 Convergência (ECG)"
                                    font_style: "H6"
                                MDLabel:
                                    id: lbl_grafico_mock
                                    text: "Gráfico: Top ↑ Média ↑\\n[Simulação de evolução]"
                                    halign: "center"
                        
                        MDCard:
                            size_hint_y: None
                            height: dp(150)
                            padding: dp(16)
                            radius: [16,]
                            MDBoxLayout:
                                orientation: 'vertical'
                                MDLabel:
                                    text: "⚠️ Anomalias"
                                    font_style: "H6"
                                ScrollView:
                                    MDLabel:
                                        id: lbl_anomalias
                                        text: "Nenhuma anomalia ainda. Inicie o motor!"
                                        size_hint_y: None
                                        height: self.texture_size[1]
                        
                        MDBoxLayout:
                            size_hint_y: None
                            height: dp(48)
                            spacing: dp(8)
                            MDFillRoundFlatButton:
                                text: "▶️ Iniciar Motor"
                                md_bg_color: 0.16, 0.65, 0.27, 1
                                on_release: app.iniciar_motor()
                            MDFillRoundFlatButton:
                                text: "⏸️ Pausar"
                                md_bg_color: 1, 0.76, 0.03, 1
                                on_release: app.pausar_motor()
                            MDFillRoundFlatButton:
                                text: "⏹️ Parar"
                                md_bg_color: 0.86, 0.21, 0.27, 1
                                on_release: app.parar_motor()
            
            MDBottomNavigationItem:
                name: 'gerador'
                text: 'Gerador'
                icon: 'auto-fix'
                
                ScrollView:
                    MDBoxLayout:
                        orientation: 'vertical'
                        adaptive_height: True
                        padding: dp(16)
                        spacing: dp(16)
                        
                        MDCard:
                            size_hint_y: None
                            height: dp(220)
                            padding: dp(16)
                            radius: [16,]
                            MDBoxLayout:
                                orientation: 'vertical'
                                spacing: dp(8)
                                MDLabel:
                                    text: "🧬 Engenharia de DNA"
                                    font_style: "H6"
                                MDTextField:
                                    id: entry_qtd
                                    hint_text: "Qtd Jogos (10 free, 33 pro)"
                                    text: "10"
                                    helper_text: "Free até 10, Pro até 33"
                                MDTextField:
                                    id: entry_fixas
                                    hint_text: "Fixas: 01, 02, 03"
                                MDTextField:
                                    id: entry_bloqueadas
                                    hint_text: "Bloqueadas: 25"
                        
                        MDCard:
                            size_hint_y: None
                            height: dp(280)
                            padding: dp(16)
                            radius: [16,]
                            MDBoxLayout:
                                orientation: 'vertical'
                                spacing: dp(4)
                                MDLabel:
                                    text: "🎛️ Filtros e Estratégia"
                                    font_style: "H6"
                                MDBoxLayout:
                                    MDCheckbox:
                                        id: chk_impar
                                        size_hint: None, None
                                        size: dp(48), dp(48)
                                    MDLabel:
                                        text: "Ímpares (7-8)"
                                MDBoxLayout:
                                    MDCheckbox:
                                        id: chk_moldura
                                    MDLabel:
                                        text: "Moldura (9-11)"
                                MDBoxLayout:
                                    MDCheckbox:
                                        id: chk_primos
                                    MDLabel:
                                        text: "Primos (4-6)"
                                MDBoxLayout:
                                    MDCheckbox:
                                        id: chk_foco14
                                    MDLabel:
                                        text: "🎯 Cofre Seguro (Foco 14)"
                                MDBoxLayout:
                                    MDCheckbox:
                                        id: chk_apriori
                                    MDLabel:
                                        text: "💎 Apriori (Pro)"
                        
                        MDCard:
                            size_hint_y: None
                            height: dp(180)
                            padding: dp(16)
                            radius: [16,]
                            MDBoxLayout:
                                orientation: 'vertical'
                                MDLabel:
                                    text: "🎚️ Hiperparâmetros"
                                    font_style: "H6"
                                MDBoxLayout:
                                    MDLabel:
                                        text: "Mutação"
                                    MDSlider:
                                        id: slider_mut
                                        min: 1
                                        max: 25
                                        value: 5
                                MDBoxLayout:
                                    MDLabel:
                                        text: "Severidade"
                                    MDSlider:
                                        id: slider_sev
                                        min: 0
                                        max: 100
                                        value: 80
            
            MDBottomNavigationItem:
                name: 'inteligencia'
                text: 'IA'
                icon: 'brain'
                
                ScrollView:
                    MDBoxLayout:
                        orientation: 'vertical'
                        adaptive_height: True
                        padding: dp(16)
                        spacing: dp(16)
                        
                        MDCard:
                            padding: dp(16)
                            size_hint_y: None
                            height: dp(80)
                            radius: [16,]
                            MDBoxLayout:
                                spacing: dp(8)
                                MDFillRoundFlatButton:
                                    text: "🔄 Atrasômetro"
                                    on_release: app.rodar_atrasometro()
                                MDFillRoundFlatButton:
                                    text: "🔗 Markov"
                                    on_release: app.rodar_markov()
                                MDFillRoundFlatButton:
                                    text: "👑 Ensemble (Pro)"
                                    on_release: app.rodar_ensemble()
                        
                        MDCard:
                            padding: dp(16)
                            radius: [16,]
                            size_hint_y: None
                            height: dp(400)
                            MDBoxLayout:
                                orientation: 'vertical'
                                MDLabel:
                                    text: "🧠 Resultado IA"
                                    font_style: "H6"
                                ScrollView:
                                    MDLabel:
                                        id: lbl_ia_result
                                        text: "Clique em uma IA acima para ver resultados.\\n\\nAtrasômetro: analisa desvio padrão\\nMarkov: sinergia entre dezenas\\nEnsemble: conselho Jedi com XGBoost"
                                        size_hint_y: None
                                        height: self.texture_size[1]
                        
                        MDCard:
                            padding: dp(16)
                            radius: [16,]
                            size_hint_y: None
                            height: dp(300)
                            MDBoxLayout:
                                orientation: 'vertical'
                                MDLabel:
                                    text: "🔥 Heatmap 5x5"
                                    font_style: "H6"
                                MDLabel:
                                    id: lbl_heatmap
                                    text: "01 02 03 04 05\\n06 07 08 09 10\\n11 12 13 14 15\\n16 17 18 19 20\\n21 22 23 24 25\\n\\n(Cores baseadas em frequência)"
                                    halign: "center"
                                    font_style: "H6"
            
            MDBottomNavigationItem:
                name: 'ranking'
                text: 'Ranking'
                icon: 'trophy'
                
                MDBoxLayout:
                    orientation: 'vertical'
                    padding: dp(16)
                    spacing: dp(8)
                    
                    MDBoxLayout:
                        size_hint_y: None
                        height: dp(48)
                        spacing: dp(8)
                        MDFillRoundFlatButton:
                            text: "🔄 Atualizar"
                            on_release: app.atualizar_ranking()
                        MDFillRoundFlatButton:
                            text: "📤 Exportar"
                            on_release: app.exportar_ranking()
                    
                    ScrollView:
                        MDBoxLayout:
                            id: box_ranking
                            orientation: 'vertical'
                            adaptive_height: True
                            spacing: dp(8)
            
            MDBottomNavigationItem:
                name: 'premium'
                text: 'Premium'
                icon: 'star'
                
                ScrollView:
                    MDBoxLayout:
                        orientation: 'vertical'
                        adaptive_height: True
                        padding: dp(16)
                        spacing: dp(16)
                        
                        MDCard:
                            padding: dp(24)
                            radius: [24,]
                            md_bg_color: 1, 0.84, 0, 0.2
                            MDBoxLayout:
                                orientation: 'vertical'
                                spacing: dp(12)
                                MDLabel:
                                    text: "👑 Lotofácil Pro Premium"
                                    font_style: "H5"
                                    bold: True
                                    halign: "center"
                                MDLabel:
                                    text: "Desbloqueie o potencial máximo"
                                    halign: "center"
                                MDLabel:
                                    text: "✅ 33 jogos (vs 10 free)\\n✅ IA completa (Ensemble, Apriori, Auto-Piloto)\\n✅ Gerações ilimitadas\\n✅ Sem anúncios\\n✅ Export CSV/PDF\\n✅ Turbo mode\\n✅ Suporte prioritário"
                                MDFillRoundFlatButton:
                                    text: "Assinar Anual R$99 (58% OFF)"
                                    md_bg_color: 0.42, 0.26, 0.76, 1
                                    pos_hint: {"center_x": 0.5}
                                    on_release: app.comprar_premium("anual")
                                MDFillRoundFlatButton:
                                    text: "Assinar Mensal R$19,90"
                                    md_bg_color: 0.2, 0.2, 0.2, 1
                                    pos_hint: {"center_x": 0.5}
                                    on_release: app.comprar_premium("mensal")
                                MDFillRoundFlatButton:
                                    text: "Vitalício R$199"
                                    md_bg_color: 0.16, 0.65, 0.27, 1
                                    pos_hint: {"center_x": 0.5}
                                    on_release: app.comprar_premium("vitalicio")
'''

class LotofacilApp(MDApp):
    rodando = BooleanProperty(False)
    geracao_atual = NumericProperty(0)
    top_score = NumericProperty(0.0)

    def build(self):
        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.theme_style = "Dark"
        self.title = "Lotofácil Pro MVP"
        self.populacao = []
        self.melhor_score = 0
        self.geracao = 0
        self.ranking = []  # lista de matrizes salvas
        return Builder.load_string(KV)

    def iniciar_motor(self):
        if self.rodando:
            return
        self.rodando = True
        self.geracao = 0
        self.melhor_score = 0
        self.log_anomalia("🚀 Motor iniciado!")
        # Inicia thread
        threading.Thread(target=self.loop_genetico, daemon=True).start()

    def pausar_motor(self):
        self.rodando = False
        self.log_anomalia("⏸️ Pausado")

    def parar_motor(self):
        self.rodando = False
        self.geracao = 0
        self.log_anomalia("⏹️ Parado")

    def loop_genetico(self):
        """Loop simplificado para MVP."""
        qtd_jogos = 10
        try:
            qtd_jogos = int(self.root.ids.entry_qtd.text)
            if qtd_jogos > 10:
                # Free limita 10
                self.log_anomalia("⚠️ Free limita 10 jogos. Assine Pro para 33!")
                qtd_jogos = 10
                Clock.schedule_once(lambda dt: setattr(self.root.ids.entry_qtd, 'text', '10'))
        except:
            qtd_jogos = 10

        # Mock populacao
        pop = [set(random.sample(range(1, 26), 20)) for _ in range(20)]
        
        while self.rodando and self.geracao < 100:
            # Simula avaliação
            scores = []
            for individuo in pop:
                # Score mock baseado em soma e aleatoriedade
                soma = sum(individuo)
                score = random.uniform(-100, 500) + (50 if 180 <= soma <= 220 else -50)
                scores.append((individuo, score))
            
            scores.sort(key=lambda x: x[1], reverse=True)
            melhor, score = scores[0]
            
            if score > self.melhor_score:
                self.melhor_score = score
                # Salva no ranking
                self.ranking.append({
                    "score": score,
                    "base_20": sorted(list(melhor)),
                    "geracao": self.geracao
                })
                self.ranking.sort(key=lambda x: x["score"], reverse=True)
                self.ranking = self.ranking[:50]

            self.geracao += 1

            # Atualiza UI via Clock
            def update_ui(dt, g=self.geracao, s=score, ms=self.melhor_score):
                try:
                    self.root.ids.lbl_geracao.text = f"Geração: {g}"
                    self.root.ids.lbl_top_score.text = f"R$ {ms:.2f}"
                    self.root.ids.lbl_grafico_mock.text = f"Geração {g}\\nTop: R${ms:.2f}\\nAtual: R${s:.2f}"
                    if ms > 0 and g % 10 == 0:
                        self.log_anomalia(f"💰 Novo top na G{g}: R${ms:.2f}")
                except:
                    pass

            Clock.schedule_once(update_ui)

            # Evolução simples
            elite = [x[0] for x in scores[:5]]
            nova = elite.copy()
            while len(nova) < 20:
                pai, mae = random.sample(elite, 2)
                filho = self.crossover_mock(pai, mae)
                filho = self.mutacao_mock(filho, 0.05)
                nova.append(filho)
            pop = nova

            time.sleep(0.5)  # simula tempo

        self.rodando = False
        Clock.schedule_once(lambda dt: self.log_anomalia("✅ Motor finalizado!"))

    def crossover_mock(self, pai, mae):
        l1, l2 = list(pai), list(mae)
        random.shuffle(l1)
        random.shuffle(l2)
        novo = set()
        for n in l1 + l2:
            if len(novo) < 20:
                novo.add(n)
        while len(novo) < 20:
            novo.add(random.randint(1, 25))
        return novo

    def mutacao_mock(self, ind, taxa):
        novo = set(ind)
        for _ in range(len(novo)):
            if random.random() < taxa:
                novo.remove(random.choice(list(novo)))
                novo.add(random.randint(1, 25))
        return novo

    def log_anomalia(self, texto):
        def update(dt):
            try:
                self.root.ids.lbl_anomalias.text += f"\\n[{time.strftime('%H:%M:%S')}] {texto}"
            except:
                pass
        Clock.schedule_once(update)

    def rodar_atrasometro(self):
        self.root.ids.lbl_ia_result.text = "🔄 Rodando Atrasômetro...\\n"
        def worker():
            time.sleep(1)
            resultado = "📊 ATRASÔMETRO - Top Dezenas para estourar:\\n\\n"
            for i in range(5):
                dezena = random.randint(1, 25)
                resultado += f"Dezena {dezena:02d} | Atraso: {random.randint(5,20)} | Status: ESTOURANDO\\n"
            Clock.schedule_once(lambda dt: setattr(self.root.ids.lbl_ia_result, 'text', resultado))
            Clock.schedule_once(lambda dt: self.log_anomalia("📊 Atrasômetro finalizado"))
        threading.Thread(target=worker, daemon=True).start()

    def rodar_markov(self):
        self.root.ids.lbl_ia_result.text = "🔗 Rodando Markov...\\n"
        def worker():
            time.sleep(1.5)
            resultado = "🔗 MARKOV - Sinergia:\\n\\n"
            for i in range(5):
                d = random.randint(1, 25)
                resultado += f"Dezena {d:02d} | Peso: {random.random():.4f}\\n"
            Clock.schedule_once(lambda dt: setattr(self.root.ids.lbl_ia_result, 'text', resultado))
        threading.Thread(target=worker, daemon=True).start()

    def rodar_ensemble(self):
        # Verifica premium
        self.root.ids.lbl_ia_result.text = "👑 Ensemble é Pro! Assine para desbloquear.\\n\\nMas aqui vai preview:\\n"
        def worker():
            time.sleep(1)
            resultado = self.root.ids.lbl_ia_result.text + "\\n🏆 Conselho Jedi - Top 5:\\n"
            top5 = random.sample(range(1, 26), 5)
            for d in top5:
                resultado += f"[{d:02d}] ⭐ {random.uniform(60,99):.1f} pts\\n"
            Clock.schedule_once(lambda dt: setattr(self.root.ids.lbl_ia_result, 'text', resultado))
        threading.Thread(target=worker, daemon=True).start()

    def atualizar_ranking(self):
        box = self.root.ids.box_ranking
        box.clear_widgets()
        if not self.ranking:
            box.add_widget(MDLabel(text="Nenhuma matriz ainda. Gere no Dashboard!", halign="center"))
            return
        for idx, item in enumerate(self.ranking[:20]):
            card = MDCard(
                size_hint_y=None,
                height=80,
                padding=12,
                spacing=8,
                radius=[12,],
            )
            from kivymd.uix.boxlayout import MDBoxLayout
            layout = MDBoxLayout(orientation='vertical')
            layout.add_widget(MDLabel(text=f"#{idx+1} - R$ {item['score']:.2f} - G{item['geracao']}", bold=True))
            layout.add_widget(MDLabel(text=f"Base: {' '.join([f'{n:02d}' for n in item['base_20'][:10]])}...", font_size="12sp"))
            card.add_widget(layout)
            box.add_widget(card)

    def exportar_ranking(self):
        self.log_anomalia("📤 Export Pro: assine para exportar CSV/PDF")

    def comprar_premium(self, tipo):
        self.log_anomalia(f"💳 Compra {tipo} - Em breve! Integração Play Billing")
        # Aqui integraria com Plyer ou android billing

    def show_config(self):
        self.log_anomalia("⚙️ Configurações - Tema, idioma, etc (em breve)")

if __name__ == '__main__':
    LotofacilApp().run()
