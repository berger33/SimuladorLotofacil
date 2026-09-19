# 🎨 DESIGN SYSTEM - Lotofácil Pro App

## 1. Princípios

- **Profissional, não amador:** Inspiração em TradingView, Binance, Notion - escuro, dados densos mas organizados
- **IA como protagonista:** Roxo + ciano + ouro, gradientes, glassmorphism sutil
- **Clareza acima de tudo:** Usuário leigo entende em 5 minutos, expert tem profundidade
- **Mobile first:** Polegar alcança tudo, bottom navigation, gestures

## 2. Cores - Material 3

### Paleta Principal
```dart
// lib/core/constants/colors.dart
class AppColors {
  // Brand
  static const primary = Color(0xFF6F42C1); // roxo IA
  static const primaryLight = Color(0xFF9A6BFF);
  static const primaryDark = Color(0xFF4A1A8B);
  
  static const secondary = Color(0xFF17A2B8); // ciano Markov
  static const secondaryLight = Color(0xFF5ED5E8);
  
  static const tertiary = Color(0xFFFFD700); // ouro Apriori
  static const tertiaryLight = Color(0xFFFFE55C);
  
  // Semânticas
  static const success = Color(0xFF28A745);
  static const warning = Color(0xFFFFC107);
  static const error = Color(0xFFDC3545);
  static const info = Color(0xFF0DCAF0);
  
  // Neutras Dark
  static const backgroundDark = Color(0xFF121212);
  static const surfaceDark = Color(0xFF1E1E1E);
  static const surfaceVariantDark = Color(0xFF2D2D2D);
  static const onBackgroundDark = Color(0xFFE0E0E0);
  static const onSurfaceDark = Color(0xFFFFFFFF);
  
  // Neutras Light
  static const backgroundLight = Color(0xFFFAFAFA);
  static const surfaceLight = Color(0xFFFFFFFF);
  static const surfaceVariantLight = Color(0xFFF0F0F0);
  static const onBackgroundLight = Color(0xFF121212);
  static const onSurfaceLight = Color(0xFF1E1E1E);
  
  // Heatmap
  static const heatCold = Color(0xFF4DABF7); // fria
  static const heatWarm = Color(0xFFFFC107);
  static const heatHot = Color(0xFFFD7E14);
  static const heatBurn = Color(0xFFDC3545); // quente
  
  // Gradientes
  static const gradientPrimary = LinearGradient(
    colors: [primary, primaryDark],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );
  static const gradientGold = LinearGradient(
    colors: [tertiary, Color(0xFFFFA000)],
  );
}
```

### Uso
- Primary: botões principais, sliders ativos, FAB
- Secondary: Markov, info
- Tertiary: destaque premium, Apriori, Top 1
- Success: lucro positivo, 14/15 pontos
- Error: prejuízo, anomalia crítica
- Heatmap: 5 níveis de intensidade

## 3. Tipografia

```dart
// lib/core/theme/text_theme.dart
import 'package:google_fonts/google_fonts.dart';

class AppTextTheme {
  static final dark = TextTheme(
    displayLarge: GoogleFonts.outfit(
      fontSize: 32, fontWeight: FontWeight.bold, color: AppColors.onBackgroundDark,
    ),
    headlineMedium: GoogleFonts.sora(
      fontSize: 24, fontWeight: FontWeight.w600,
    ),
    titleLarge: GoogleFonts.sora(
      fontSize: 20, fontWeight: FontWeight.w600,
    ),
    bodyLarge: GoogleFonts.inter(
      fontSize: 16, fontWeight: FontWeight.normal,
    ),
    bodyMedium: GoogleFonts.inter(
      fontSize: 14,
    ),
    labelLarge: GoogleFonts.inter(
      fontSize: 14, fontWeight: FontWeight.w600,
    ),
    // Mono para números
    bodySmall: GoogleFonts.jetBrainsMono(
      fontSize: 12,
    ),
  );
}
```

- **Outfit:** títulos, impacto
- **Sora:** subtítulos, moderno tech
- **Inter:** corpo, legibilidade
- **JetBrains Mono:** dezenas, números, logs

## 4. Componentes

### 4.1 Bottom Navigation (5 itens)
- Dashboard (home)
- Gerador (auto_awesome)
- Inteligência (psychology)
- Ranking (emoji_events)
- Premium (workspace_premium) - se já premium, mostra Configurações (settings)

### 4.2 Cards
```dart
Card(
  elevation: 2,
  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
  child: ...
)
```

- **CardMatriz:** mostra posição, saldo com cor (verde se >0), base 20 em chips, stats 11-15
- **CardEstatistica:** ícone + valor + label
- **CardIA:** ícone + título + descrição + score + botão Fixar

### 4.3 Chips Dezenas
- Selecionada: primary container com check
- Bloqueada: error container com X
- Fixa: tertiary container com estrela
- Normal: surface variant

### 4.4 Sliders
- Custom slider com valor em cima, thumb grande, active track gradient
- Mostra % ou valor

### 4.5 Botões
- **Filled:** ação principal (Gerar)
- **Tonal:** secundária (Pausar)
- **Outlined:** terciária (Cancelar)
- **Text:** link
- **FAB:** Turbo

### 4.6 Heatmap 5x5
- Grid 5 colunas
- Cada célula 48dp, border radius 12
- Cor baseada em frequência normalizada
- Animação: scale ao atualizar
- Ao tocar: mostra tooltip com dezena e frequência

### 4.7 Gráfico Convergência
- `fl_chart` LineChart
- 2 linhas: Top (verde) e Média (ciano)
- Área com gradiente
- Eixo X: gerações, Y: lucro
- Touch tooltip
- Animação 300ms

### 4.8 Empty States
- Ilustração (Lottie ou SVG)
- Título: "Nenhuma matriz ainda"
- Sub: "Gere sua primeira matriz no Gerador"
- Botão CTA

### 4.9 Loading
- Shimmer para listas
- CircularProgressIndicator com label
- Lottie foguete para geração

### 4.10 Paywall
- Bottom sheet modal, não full screen (menos agressivo)
- Header com gradiente + ícone premium
- Lista benefícios com ícones check
- Preços em cards, anual com badge "MAIS POPULAR"
- Botão CTA sticky bottom

## 5. Telas - Wireframes Textuais

### Onboarding
```
[Logo Lottie]
Título: "Bem-vindo ao Lab"
Sub: "Análise inteligente para Lotofácil"
[Indicador 1/3]
[Botão Próximo]
```

### Dashboard
```
[AppBar: Logo + sino notificações + avatar premium]

[Card Saldo: R$1.234 + Gráfico mini]
[Row: 3 cards: Top, Média, Drawdown]

[Seção Último Sorteio: 15 bolas + data]

[Seção Gráfico Convergência - Card grande]

[Seção Anomalias: lista 3 últimas]

[Seção Atalhos: 3 botões: Gerar, IA, Ranking]

[Banner AdMob se free]
```

### Gerador
```
[AppBar: Gerador + botão info]

[Segment: Qtd Jogos: 10 | 15 | 20 | 33 (33 com ícone premium)]

[Card DNA:
  Fixas: [chips] + botão +
  Bloqueadas: [chips] + botão +
]

[Card Filtros:
  Título + toggle Auto-Piloto (premium)
  Grid chips: Ímpares, Moldura, Primos, Soma, Seq, Fibonacci
]

[Card Hiperparâmetros:
  Mutação: [slider 1-25%]
  Severidade: [slider 0-100%]
  Switches: Memória, Hamming, Foco 14
]

[Card Estratégia:
  Lista: Conservador, Agressivo, Robô Preguiçoso (selecionável)
]

[Botão grande: Iniciar Motor Híbrido]

[Bottom sheet ao iniciar: logs + progresso + botões Pausar/Parar]
```

### Inteligência
```
[AppBar: Inteligência]

[TabBar: Atrasômetro | Markov | Ensemble | Apriori]

[Conteúdo:
  Card explicação
  Lista: Dezena | Score | Status
  Botão: Fixar Top 5
]

[Heatmap no bottom ou aba separada]
```

### Ranking
```
[AppBar: Ranking + filtro ecossistema (dropdown) + botão atualizar]

[Segment: Top 50 | Top 3 | Favoritos]

[Lista cards matriz]

[Ao clicar card -> Detalhes]

Detalhes:
[AppBar: Detalhes + botões favoritar, compartilhar, deletar]
[Card: Posição, Saldo, Stats]
[Card: Base 20 em destaque grande]
[Lista: Jogos 01: [01 02 ...] com botão copiar]
[Row botões: Stress Histórico, Caos, Bootstrap]
[Área resultado stress]
[Botões: Export CSV, Compartilhar]
```

## 6. Animações e Micro-interações

- **Transições:** Fade + slide 300ms, easing easeInOut
- **Hero:** Card matriz -> detalhes
- **Confetti:** Quando 15 pontos em stress test
- **Haptic:** Leve vibração ao gerar, ao atingir novo top
- **Skeleton:** Ao carregar listas
- **Pull to refresh:** Dashboard e Ranking

## 7. Acessibilidade

- Content description em todos ícones
- Tamanho mínimo toque 48dp
- Contraste AA (4.5:1)
- Suporte TalkBack / VoiceOver
- Texto escalável (não fixo)
- Navegação por teclado (para ChromeOS)

## 8. Ícone e Branding

- **Nome:** Lotofácil Pro
- **Sub:** IA & Estatística
- **Logo:** L + gráfico + estrela, roxo gradiente
- **Slogan:** "Onde a matemática encontra a sorte"
- **Tom de voz:** Técnico mas acessível, confiante mas não promete ganhos, educacional

## 9. Ferramentas Design

- Figma para protótipo
- LottieFiles para animações
- Material Symbols para ícones
- Coolors para paleta
- Mobbin para inspiração apps financeiros
```

## 10. Checklist UI Profissional

- [ ] Dark/light theme com Material 3
- [ ] Onboarding 3 telas + disclaimer
- [ ] Empty states
- [ ] Loading states
- [ ] Error states com retry
- [ ] Offline indicator
- [ ] Shimmer
- [ ] Pull to refresh
- [ ] Haptic feedback
- [ ] Animações 60fps
- [ ] Ícone adaptativo Android
- [ ] Splash screen
