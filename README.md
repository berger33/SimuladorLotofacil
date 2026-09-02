<div align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Machine%20Learning-XGBoost-orange.svg" alt="XGBoost">
  <img src="https://img.shields.io/badge/Algoritmo-Gen%C3%A9tico-brightgreen.svg" alt="Genetic Algorithm">
  <img src="https://img.shields.io/badge/Reinforcement-Learning-purple.svg" alt="Q-Learning">
  
  <h1>🎰 Simulador Lotofácil Pro </h1>
  <p><i>Um ecossistema preditivo de última geração alimentado por Inteligência Artificial e Algoritmos Genéticos para encontrar padrões estatísticos de alta performance na Lotofácil.</i></p>
</div>

---

## 🚀 O que é o Simulador Lotofácil Pro?
O **Lotofácil Pro** não é apenas um gerador de desdobramentos. É uma ferramenta analítica que simula milhões de sorteios e evolui "Matrizes Genéticas" utilizando a teoria da evolução de Darwin. Para completar, o sistema é injetado com **Machine Learning** de ponta para prever padrões ocultos.

Se você gosta de matemática, estatística e inteligência artificial, este é o laboratório definitivo.

---

## ✨ Principais Funcionalidades (O "Cérebro" da Máquina)

### 🧬 Algoritmo Genético (Evolução Contínua)
O simulador cria uma população de "jogos" (cromossomos). Aqueles que ganham menos são sumariamente descartados. Os que dão lucro sofrem **Crossover** e **Mutação**, repassando seus "genes" vencedores para a próxima geração. 

### 🤖 Inteligências Artificiais e Machine Learning
- **Atrasômetro (Desvio Padrão):** Analisa a variância de cada dezena.
- **Cadeias de Markov:** Calcula a sinergia entre dezenas (Probabilidade Condicional).
- **Ensemble Híbrido (XGBoost):** Árvores de decisão que cruzam Markov com Atraso para eleger o *Top 5* dezenas supremas.
- **Mineração Apriori (Combos de Ouro):** Varre a história da loteria caçando *Trincas* que sempre saem juntas, recompensando jogos que tiverem essas combinações.
- **Auto-Piloto de Filtros:** Um Regressor prevê o número *exato* de Ímpares, Primos, etc., para o próximo sorteio.
- **Q-Learning (IA Autônoma):** Um Agente de Reinforcement Learning que auto-calibra a mutação e a severidade com base no que está dando mais lucro no momento!

---

## 🛠️ Instalação e Execução

### Pré-requisitos
- Python 3.10+
- Pip instalado

### 1. Clonando o Repositório
```bash
git clone https://github.com/berger33/Lotofacil_Pro.git
cd Lotofacil_Pro
```

### 2. Instalando Dependências
```bash
pip install -r requirements.txt
```
*(Caso o arquivo não exista, instale os principais manualmente: `pip install customtkinter numpy xgboost optuna pytest`)*

### 3. Rodando o Simulador
```bash
python main.py
```

---

## 📖 Como Usar? (Manual de Operação)
Para entender profundamente como usar cada chave do sistema e maximizar seus resultados, leia o **[Tutorial Completo (TUTORIAL.md)](TUTORIAL.md)**.

---

## 🏗️ Estrutura do Projeto
- `main.py` - Ponto de entrada.
- `ui/interface.py` - O "Cockpit", painel de controle feito em CustomTkinter.
- `core/engine.py` - O Motor Híbrido, gerencia as threads e as gerações.
- `core/genetic.py` - As leis de Crossover e Mutação.
- `core/evaluator.py` - O Juiz. Mede o "Fitness" (Lucratividade) de cada jogo.
- `core/ml_intelligence.py` - Todos os modelos de Machine Learning.
- `core/rl_agent.py` - A IA autônoma Q-Learning que auto-configura o sistema.

---

## 🛡️ Aviso Legal
Este software é um **laboratório de simulação estatística e estudo de Machine Learning**.
A loteria é um jogo de azar de eventos independentes. O uso desta ferramenta não garante ganhos financeiros. Não aposte dinheiro que você não pode perder.

---
<div align="center">
<i>Desenvolvido com ☕ e IA Avançada.</i>
</div>
