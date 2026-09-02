# 📚 Tutorial de Operação do Lotofácil Pro V11

Bem-vindo ao **Lotofácil Pro**. A interface deste software foi inspirada no cockpit de um avião: pode parecer complexa à primeira vista, mas cada chave possui uma função estatística muito específica.

Este tutorial ensinará você a dominar a máquina, compreendendo as funções isoladamente e, mais importante, **como combiná-las para criar estratégias imbatíveis**.

---

## 🔬 1. Entendendo o Básico: O Algoritmo Genético
Quando você clica em **"▶️ Iniciar Motor Híbrido"**, o sistema não "gera cartelas aleatórias". Ele faz o seguinte:
1. Gera centenas de cartelas "mãe".
2. Pega essas cartelas e joga contra todos os sorteios do histórico da Lotofácil (ou joga simulando contra o futuro).
3. Corta as cartelas que deram prejuízo financeiro.
4. Pega as que deram lucro e faz **"Sexo Genético" (Crossover)** entre elas e aplica **Mutação**, gerando os "filhos" (a próxima geração).
5. O ciclo repete para sempre até você parar. O lucro médio vai subindo a cada geração!

### 🎚️ Sliders de Controle (À esquerda)
- **Taxa de Mutação (1% a 25%):** O quanto o DNA dos filhos sofrerá alterações aleatórias. Se o lucro estiver subindo devagar, aumente a mutação para dar "choques" no sistema. Se estiver lucrando bem, diminua para estabilizar.
- **Severidade na Punição (0 a 100%):** O quão dura a máquina deve ser. Em 100%, se uma dezena fez a cartela perder dinheiro, a máquina cria um ódio mortal por ela e tenta bani-la para sempre.

---

## 🧮 2. Filtros e Fechamento (Lado Esquerdo)
Você verá diversas caixas de seleção, como **Ímpares (7 a 8)**, **Primos (4 a 6)**, **Soma (180 a 210)**. 
- Se você ativar a caixa, o motor genético *só permitirá que nasçam cartelas que obedeçam a essas regras matemáticas*. 
- **⚠️ Aviso:** Se você ligar TODOS os filtros de uma vez e travar as dezenas bloqueadas, a máquina pode não conseguir encontrar nenhum jogo viável na Terra. Nesse caso, a máquina usará uma inteligência que "relaxa" a regra gradualmente (Ex: se não acha 7 ímpares, ela relaxa para 6 ou 9 para poder continuar).

### 🎯 Estratégia Cofre Seguro (Foco 14 Pontos)
Na Lotofácil real, acertar 15 pontos é dificílimo (1 em 3.2 milhões).
Ao ligar esta chave, você diz para a IA: *"Não ligue para o prêmio de 15 pontos"*. O algoritmo zera o prêmio de 15 na mente dele e passa a buscar e cruzar SOMENTE jogos que dão 14 pontos com uma frequência altíssima. É perfeito para quem quer retorno garantido ao invés de buscar a loteria.

---

## 🧠 3. As Chaves de Inteligência Artificial (Lado Direito)
Aqui está a mágica do sistema. Você não precisa pensar, a máquina pensa por você.

### ⏱️ O Atrasômetro Analítico
Verifica quais dezenas estão presas e prestes a estourar baseado em desvio padrão matemático. Use para escolher suas dezenas **Fixas** manualmente.

### 🔗 IA Markov (Previsão de Fluxo)
O algoritmo usa "Probabilidade Condicional". Exemplo: *Ele descobre que toda vez que a bola 04 sai, a bola 22 tem 80% de chance de sair logo depois.*
- Ao ativar, a máquina injeta as dezenas mais "amigas" umas das outras no sistema.

### 👑 Ensemble Híbrido (O Conselho Jedi)
Se você não sabe qual IA usar, ative o Ensemble. Ele pega a opinião do Atrasômetro, a opinião da IA Markov, e a opinião de uma Árvore de Decisão XGBoost, vota, e entrega as **Top 5 Dezenas Supremas**.

---

## 💎 4. As Super IAs Autônomas (O "Auto-Piloto")
Na parte inferior direita, você tem os botões que transformam o simulador em um robô 100% autônomo.

### 💎 Mineração Apriori (Combos de Ouro)
A IA olha para os últimos 500 sorteios e caça **Trincas (grupos de 3 números)** que estão saindo igual água (Ex: 01, 10, 25).
Quando a IA Genética cria um filho, ela dá um bônus imenso de pontuação se ele tiver essa Trinca. O resultado? Os jogos finais virão recheados com os padrões mais fortes do histórico.

### 🎯 Auto-Piloto de Filtros (XGBoost)
*Substitui a adivinhação humana dos Filtros do lado esquerdo.*
Em vez de VOCÊ escolher "Soma de 180 a 210", o modelo de Machine Learning vai olhar para as marés dos sorteios e dizer: *"A tendência diz que amanhã a soma será exatamente 198"*. E os filtros do motor vão se ajustar para travar **apenas matrizes que dão soma 198**. É brutal!

### 🤖 IA Autônoma (Rede Neural Profunda PyTorch)
Você não sabe se deve colocar a Mutação em 5% ou 15%? 
Ative isso! A Inteligência Artificial (Deep Reinforcement Learning) vai assumir os controles. Ela vai testar a Mutação alta, vai ver que deu prejuízo, vai se punir matematicamente pelo PyTorch, e vai trocar sozinha para Mutação baixa. Ela guarda as conexões neurais na memória (`storage/dqn_model.pth`) contendo o que funciona. Deixe rodando por horas e o software ficará incrivelmente inteligente.

---

## 🚀 Como usar tudo isso junto? (Cenários Reais)

### Cenário 1: "O Robô Preguiçoso" (Deixa a IA fazer tudo)
Se você quer ir tomar um café e deixar a máquina encontrar a perfeição:
1. Ative **🎯 Auto-Piloto de Filtros**
2. Ative **💎 Mineração Apriori**
3. Ative **🤖 IA Autônoma (Rede Neural Profunda PyTorch)**
4. Selecione **Quantidade de Jogos: 15** (para jogar baratinho na lotérica).
5. Clique em Iniciar. A máquina vai definir os filtros, vai achar as trincas secretas, vai configurar a mutação sozinha e vai entregar a cartela pronta na aba "Melhores".

### Cenário 2: "O Investidor Conservador" (Cofre Seguro)
1. Ative os filtros **Ímpares, Moldura e Primos** manualmente.
2. Ative **🎯 Estratégia Cofre Seguro (Foco 14)** (Para focar em fechar os 14 pontos).
3. Ative **👑 Ensemble Híbrido** (A IA colocará 5 dezenas quentes como Fixas na sua cartela).
4. **Severidade: 100%**. Você será um general implacável; as cartelas erradas vão morrer rápido.
5. Inicie o sistema.

---

## ❓ FAQ & Solução de Problemas

**O sistema está muito lento! O que eu faço?**
A Inteligência Artificial exige bastante da CPU do computador. O sistema possui um modo **Turbo (Múltiplos Núcleos)** que você pode ativar na interface (Modo Fúria). Se mesmo assim estiver lento, diminua o número de `População` no arquivo `config.py`.

**Por que o "Foco 14" diminui o lucro estimado na tela?**
Porque ele ignora (zera) a premiação raríssima de 15 pontos do cálculo. É uma estimativa mais realista e pessimista, mostrando o que você ganharia no "pior cenário" fechando só prêmios menores.

**A Rede Neural da IA Autônoma reseta se eu fechar o programa?**
Não! Ela salva o aprendizado em `storage/dqn_model.pth`. O seu robô manterá o aprendizado das madrugadas passadas.

*Divirta-se quebrando padrões!* 🎰🧠
