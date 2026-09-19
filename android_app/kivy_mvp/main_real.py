"""
KivyMD MVP REAL - usando core_shared de verdade
Mesma UI do main.py mas com motor real, não mock
"""
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import BooleanProperty, NumericProperty
from kivymd.app import MDApp
import threading
import sys
import os
import time
import random

# Add core_shared
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from core_shared.data.repository import LocalJsonRepository
    from core_shared.data.crawler import carregar_sorteios_com_fallback
    from core_shared.engine.engine import MotorLotofacilLite
    from core_shared.domain.models import ConfigGeracao, Filtros
    from core_shared.domain.enums import ModoTreino
    from core_shared.ml.atrasometro import analisar_atrasos
    from core_shared.ml.markov import gerar_previsao_markov
    from core_shared.ml.ensemble_lite import executar_ensemble_hibrido
    CORE_AVAILABLE = True
except ImportError as e:
    print(f"core_shared falhou: {e}")
    CORE_AVAILABLE = False

KV_REAL = '''
MDScreen:
    MDBoxLayout:
        orientation: 'vertical'
        
        MDTopAppBar:
            title: "Lotofácil Pro - REAL"
            left_action_items: [["menu", lambda x: None]]
            right_action_items: [["cog", lambda x: app.show_config()]]
        
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
                                    text: "Top Score (REAL)"
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
                                    text: "Geração: 0 | Sorteios: 0"
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
                                    text: "📊 Motor Real - core_shared"
                                    font_style: "H6"
                                MDLabel:
                                    id: lbl_grafico_mock
                                    text: "Usando MotorLotofacilLite real\\ncom sorteios da Caixa"
                                    halign: "center"
                        
                        MDCard:
                            size_hint_y: None
                            height: dp(150)
                            padding: dp(16)
                            radius: [16,]
                            MDBoxLayout:
                                orientation: 'vertical'
                                MDLabel:
                                    text: "⚠️ Logs Reais"
                                    font_style: "H6"
                                ScrollView:
                                    MDLabel:
                                        id: lbl_anomalias
                                        text: "Motor real carregado. Sorteios: cache + API Caixa"
                                        size_hint_y: None
                                        height: self.texture_size[1]
                        
                        MDBoxLayout:
                            size_hint_y: None
                            height: dp(48)
                            spacing: dp(8)
                            MDFillRoundFlatButton:
                                text: "▶️ Iniciar REAL"
                                md_bg_color: 0.16, 0.65, 0.27, 1
                                on_release: app.iniciar_motor_real()
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
                                    text: "🧬 Engenharia de DNA (REAL)"
                                    font_style: "H6"
                                MDTextField:
                                    id: entry_qtd
                                    hint_text: "Qtd Jogos (10 free, 33 pro)"
                                    text: "10"
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
                                    text: "🎛️ Filtros Reais"
                                    font_style: "H6"
                                MDBoxLayout:
                                    MDCheckbox:
                                        id: chk_impar
                                    MDLabel:
                                        text: "Ímpares (7-8)"
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
                                    text: "🎚️ Hiperparâmetros Reais"
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
                text: 'IA Real'
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
                                    text: "🔄 Atrasômetro REAL"
                                    on_release: app.rodar_atrasometro_real()
                                MDFillRoundFlatButton:
                                    text: "🔗 Markov REAL"
                                    on_release: app.rodar_markov_real()
                                MDFillRoundFlatButton:
                                    text: "👑 Ensemble REAL"
                                    on_release: app.rodar_ensemble_real()
                        
                        MDCard:
                            padding: dp(16)
                            radius: [16,]
                            size_hint_y: None
                            height: dp(400)
                            MDBoxLayout:
                                orientation: 'vertical'
                                MDLabel:
                                    text: "🧠 Resultado IA Real"
                                    font_style: "H6"
                                ScrollView:
                                    MDLabel:
                                        id: lbl_ia_result
                                        text: "IA real usando sorteios da Caixa\\nClique acima"
                                        size_hint_y: None
                                        height: self.texture_size[1]
            
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
                    
                    ScrollView:
                        MDBoxLayout:
                            id: box_ranking
                            orientation: 'vertical'
                            adaptive_height: True
                            spacing: dp(8)
'''

class LotofacilRealApp(MDApp):
    rodando = BooleanProperty(False)

    def build(self):
        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.theme_style = "Dark"
        self.title = "Lotofácil Pro REAL"
        self.motor = None
        self.sorteios = []
        self.ranking = []
        
        if CORE_AVAILABLE:
            self.sorteios = carregar_sorteios_com_fallback()
        else:
            self.sorteios = [set(random.sample(range(1,26),15)) for _ in range(500)]
            
        return Builder.load_string(KV_REAL)

    def on_start(self):
        def update(dt):
            try:
                self.root.ids.lbl_geracao.text = f"Geração: 0 | Sorteios: {len(self.sorteios)} (REAL)"
                self.root.ids.lbl_anomalias.text = f"✅ {len(self.sorteios)} sorteios carregados\\nMotor: {'REAL core_shared' if CORE_AVAILABLE else 'MOCK'}"
            except:
                pass
        Clock.schedule_once(update, 1)

    def iniciar_motor_real(self):
        if self.rodando:
            return
        self.rodando = True
        self.log_anomalia("🚀 Motor REAL iniciado com core_shared!")
        threading.Thread(target=self.loop_real, daemon=True).start()

    def loop_real(self):
        if not CORE_AVAILABLE:
            self.log_anomalia("⚠️ core_shared não disponível, usando mock")
            # fallback mock loop
            for g in range(20):
                if not self.rodando:
                    break
                time.sleep(0.5)
                Clock.schedule_once(lambda dt, g=g: self.update_ui_mock(g))
            self.rodando = False
            return

        try:
            qtd = 10
            try:
                qtd = int(self.root.ids.entry_qtd.text)
                if qtd > 10:
                    qtd = 10
            except:
                qtd = 10

            fixas = []
            bloq = []
            try:
                fixas_text = self.root.ids.entry_fixas.text
                if fixas_text:
                    fixas = [int(x.strip()) for x in fixas_text.split(',') if x.strip().isdigit()]
                bloq_text = self.root.ids.entry_bloqueadas.text
                if bloq_text:
                    bloq = [int(x.strip()) for x in bloq_text.split(',') if x.strip().isdigit()]
            except:
                pass

            filtros = Filtros(
                impar=8 if self.root.ids.chk_impar.active else None,
                bloqueadas=bloq,
                fixas=fixas,
            )

            config = ConfigGeracao(
                num_jogos=qtd,
                populacao=20,  # menor para mobile
                elite=5,
                taxa_mutacao=self.root.ids.slider_mut.value / 100.0,
                severidade=self.root.ids.slider_sev.value / 100.0,
                filtros=filtros,
                foco_14=self.root.ids.chk_foco14.active,
                max_geracoes=30,
                simulacoes_por_avaliacao=200,
            )

            repo = LocalJsonRepository()
            
            def on_progress(resultado):
                def update(dt):
                    try:
                        self.root.ids.lbl_top_score.text = f"R$ {resultado.score:.2f}"
                        self.root.ids.lbl_geracao.text = f"Geração: {resultado.geracao} | Top: R$ {resultado.score:.2f}"
                        self.root.ids.lbl_grafico_mock.text = f"G{resultado.geracao} | Score R$ {resultado.score:.2f}\\n11:{resultado.stats.h11} 12:{resultado.stats.h12} 13:{resultado.stats.h13} 14:{resultado.stats.h14} 15:{resultado.stats.h15}"
                        if resultado.score > 0:
                            self.ranking.append({
                                "score": resultado.score,
                                "base_20": resultado.base_20,
                                "geracao": resultado.geracao,
                                "sistema": resultado.sistema,
                            })
                            self.ranking.sort(key=lambda x: x["score"], reverse=True)
                            self.ranking = self.ranking[:20]
                    except Exception as e:
                        print(f"UI update erro: {e}")
                Clock.schedule_once(update)

            def on_anomalia(msg):
                self.log_anomalia(msg)

            motor = MotorLotofacilLite(repository=repo, on_progress=on_progress, on_anomalia=on_anomalia)
            motor._sorteios_treino = self.sorteios
            motor._rodando = True
            self.motor = motor

            resultados = motor.gerar(config=config)
            self.log_anomalia(f"✅ Motor REAL finalizado! {len(resultados)} gerações")

        except Exception as e:
            self.log_anomalia(f"❌ Erro motor real: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.rodando = False

    def update_ui_mock(self, g):
        try:
            self.root.ids.lbl_geracao.text = f"Geração: {g} (MOCK)"
            self.root.ids.lbl_top_score.text = f"R$ {random.uniform(0,500):.2f}"
        except:
            pass

    def pausar_motor(self):
        self.rodando = False
        if self.motor:
            self.motor.pausar()
        self.log_anomalia("⏸️ Pausado")

    def parar_motor(self):
        self.rodando = False
        if self.motor:
            self.motor.parar()
        self.log_anomalia("⏹️ Parado")

    def log_anomalia(self, texto):
        def update(dt):
            try:
                import time as t
                self.root.ids.lbl_anomalias.text += f"\n[{t.strftime('%H:%M:%S')}] {texto}"
            except:
                pass
        Clock.schedule_once(update)

    def rodar_atrasometro_real(self):
        self.root.ids.lbl_ia_result.text = "🔄 Rodando Atrasômetro REAL...\n"
        def worker():
            try:
                if CORE_AVAILABLE:
                    dados, anomalias = analisar_atrasos(self.sorteios)
                    texto = f"📊 ATRASÔMETRO REAL - {len(self.sorteios)} sorteios\n\n"
                    for n, d in sorted(dados.items(), key=lambda x: x[1]['atual'], reverse=True)[:10]:
                        texto += f"Dez {n:02d} | Atual:{d['atual']:02d} Média:{d['media']:.1f} Lim:{d['limite']:.1f} {d['status']}\n"
                    if anomalias:
                        texto += f"\n🚨 ANOMALIAS: {anomalias}\n"
                else:
                    texto = "Mock atrasômetro - core_shared não disponível"
                Clock.schedule_once(lambda dt: setattr(self.root.ids.lbl_ia_result, 'text', texto))
            except Exception as e:
                Clock.schedule_once(lambda dt: setattr(self.root.ids.lbl_ia_result, 'text', f"Erro: {e}"))
        threading.Thread(target=worker, daemon=True).start()

    def rodar_markov_real(self):
        self.root.ids.lbl_ia_result.text = "🔗 Rodando Markov REAL...\n"
        def worker():
            try:
                if CORE_AVAILABLE:
                    top5, ranking = gerar_previsao_markov(self.sorteios)
                    texto = f"🔗 MARKOV REAL - Top 5: {top5}\n\n"
                    for d,p in ranking[:10]:
                        texto += f"Dez {d:02d} | Peso: {p:.4f}\n"
                else:
                    texto = "Mock markov"
                Clock.schedule_once(lambda dt: setattr(self.root.ids.lbl_ia_result, 'text', texto))
            except Exception as e:
                Clock.schedule_once(lambda dt: setattr(self.root.ids.lbl_ia_result, 'text', f"Erro: {e}"))
        threading.Thread(target=worker, daemon=True).start()

    def rodar_ensemble_real(self):
        self.root.ids.lbl_ia_result.text = "👑 Rodando Ensemble REAL (pode demorar)...\n"
        def worker():
            try:
                if CORE_AVAILABLE:
                    top5, relatorio = executar_ensemble_hibrido(self.sorteios, usar_xgboost=False)  # False para ser rápido no mobile
                    texto = relatorio
                else:
                    texto = "Mock ensemble"
                Clock.schedule_once(lambda dt: setattr(self.root.ids.lbl_ia_result, 'text', texto))
            except Exception as e:
                Clock.schedule_once(lambda dt: setattr(self.root.ids.lbl_ia_result, 'text', f"Erro: {e}"))
        threading.Thread(target=worker, daemon=True).start()

    def atualizar_ranking(self):
        try:
            box = self.root.ids.box_ranking
            box.clear_widgets()
            if not self.ranking:
                from kivymd.uix.label import MDLabel
                box.add_widget(MDLabel(text="Nenhuma matriz ainda. Gere no Dashboard!", halign="center"))
                return
            for idx, item in enumerate(self.ranking[:15]):
                from kivymd.uix.card import MDCard
                from kivymd.uix.boxlayout import MDBoxLayout
                from kivymd.uix.label import MDLabel
                card = MDCard(size_hint_y=None, height=80, padding=12, radius=[12,])
                layout = MDBoxLayout(orientation='vertical')
                layout.add_widget(MDLabel(text=f"#{idx+1} - R$ {item['score']:.2f} - G{item['geracao']}", bold=True))
                base_str = ' '.join([f"{n:02d}" for n in item['base_20'][:10]])
                layout.add_widget(MDLabel(text=f"Base: {base_str}...", font_size="12sp"))
                card.add_widget(layout)
                box.add_widget(card)
        except Exception as e:
            print(f"Erro ranking: {e}")

    def show_config(self):
        self.log_anomalia("⚙️ Configurações (em breve)")

if __name__ == '__main__':
    LotofacilRealApp().run()
