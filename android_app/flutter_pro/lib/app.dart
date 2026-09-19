import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

// Cores Material 3 - Design System
class AppColors {
  static const primary = Color(0xFF6F42C1);
  static const primaryLight = Color(0xFF9A6BFF);
  static const primaryDark = Color(0xFF4A1A8B);
  static const secondary = Color(0xFF17A2B8);
  static const tertiary = Color(0xFFFFD700);
  static const success = Color(0xFF28A745);
  static const error = Color(0xFFDC3545);
  static const backgroundDark = Color(0xFF121212);
  static const surfaceDark = Color(0xFF1E1E1E);
  static const backgroundLight = Color(0xFFFAFAFA);
}

class LotofacilProApp extends StatelessWidget {
  const LotofacilProApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Lotofácil Pro',
      debugShowCheckedModeBanner: false,
      themeMode: ThemeMode.dark,
      theme: _buildLightTheme(),
      darkTheme: _buildDarkTheme(),
      home: const MainNavigation(),
    );
  }

  ThemeData _buildDarkTheme() {
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.dark,
      primaryColor: AppColors.primary,
      scaffoldBackgroundColor: AppColors.backgroundDark,
      colorScheme: const ColorScheme.dark(
        primary: AppColors.primary,
        secondary: AppColors.secondary,
        tertiary: AppColors.tertiary,
        surface: AppColors.surfaceDark,
        background: AppColors.backgroundDark,
        error: AppColors.error,
      ),
      textTheme: GoogleFonts.interTextTheme(ThemeData.dark().textTheme),
      cardTheme: CardTheme(
        elevation: 2,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
        color: AppColors.surfaceDark,
      ),
      appBarTheme: const AppBarTheme(
        backgroundColor: AppColors.surfaceDark,
        elevation: 0,
      ),
      bottomNavigationBarTheme: const BottomNavigationBarThemeData(
        backgroundColor: AppColors.surfaceDark,
        selectedItemColor: AppColors.primaryLight,
        unselectedItemColor: Colors.grey,
      ),
    );
  }

  ThemeData _buildLightTheme() {
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.light,
      primaryColor: AppColors.primary,
      scaffoldBackgroundColor: AppColors.backgroundLight,
      colorScheme: const ColorScheme.light(
        primary: AppColors.primary,
        secondary: AppColors.secondary,
        tertiary: AppColors.tertiary,
      ),
      textTheme: GoogleFonts.interTextTheme(ThemeData.light().textTheme),
      cardTheme: CardTheme(
        elevation: 2,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      ),
    );
  }
}

// Navegação principal - 5 abas
class MainNavigation extends StatefulWidget {
  const MainNavigation({super.key});

  @override
  State<MainNavigation> createState() => _MainNavigationState();
}

class _MainNavigationState extends State<MainNavigation> {
  int _currentIndex = 0;

  final _screens = [
    const DashboardScreen(),
    const GeradorScreen(),
    const InteligenciaScreen(),
    const RankingScreen(),
    const PremiumScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _screens[_currentIndex],
      bottomNavigationBar: NavigationBar(
        selectedIndex: _currentIndex,
        onDestinationSelected: (i) => setState(() => _currentIndex = i),
        destinations: const [
          NavigationDestination(icon: Icon(Icons.dashboard), label: 'Dashboard'),
          NavigationDestination(icon: Icon(Icons.auto_fix_high), label: 'Gerador'),
          NavigationDestination(icon: Icon(Icons.psychology), label: 'IA'),
          NavigationDestination(icon: Icon(Icons.emoji_events), label: 'Ranking'),
          NavigationDestination(icon: Icon(Icons.workspace_premium), label: 'Pro'),
        ],
      ),
    );
  }
}

// Placeholders - cada um viraria arquivo separado em presentation/screens/

class DashboardScreen extends StatelessWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Dashboard'), actions: [
        IconButton(icon: const Icon(Icons.notifications), onPressed: () {}),
      ]),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          // Card Saldo
          Card(
            color: AppColors.primary,
            child: Padding(
              padding: const EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('Top Score', style: Theme.of(context).textTheme.titleMedium?.copyWith(color: Colors.white70)),
                  const SizedBox(height: 8),
                  Text('R\$ 1.234,56', style: Theme.of(context).textTheme.headlineMedium?.copyWith(color: Colors.white, fontWeight: FontWeight.bold)),
                  Text('Geração 42 • Média R\$ 320', style: Theme.of(context).textTheme.bodySmall?.copyWith(color: Colors.white70)),
                ],
              ),
            ),
          ),
          const SizedBox(height: 16),
          // Gráfico mock
          Card(
            child: SizedBox(
              height: 200,
              child: Center(child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(Icons.show_chart, size: 48, color: AppColors.success),
                  const SizedBox(height: 8),
                  Text('Convergência (ECG)', style: Theme.of(context).textTheme.titleMedium),
                  const Text('Top ↑ Média ↑ - fl_chart aqui'),
                ],
              )),
            ),
          ),
          const SizedBox(height: 16),
          Card(
            child: ListTile(
              leading: const Icon(Icons.warning, color: AppColors.tertiary),
              title: const Text('Anomalias'),
              subtitle: const Text('Nenhuma anomalia crítica. Sistema saudável.'),
            ),
          ),
          const SizedBox(height: 16),
          // Banner Ad placeholder
          Container(
            height: 50,
            decoration: BoxDecoration(color: Colors.grey[800], borderRadius: BorderRadius.circular(8)),
            child: const Center(child: Text('AdMob Banner (Free)', style: TextStyle(color: Colors.white54))),
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () {},
        icon: const Icon(Icons.play_arrow),
        label: const Text('Gerar'),
      ),
    );
  }
}

class GeradorScreen extends StatelessWidget {
  const GeradorScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Gerador')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('🧬 Engenharia de DNA', style: Theme.of(context).textTheme.titleLarge),
                  const SizedBox(height: 12),
                  SegmentedButton<int>(
                    segments: const [
                      ButtonSegment(value: 10, label: Text('10 Free')),
                      ButtonSegment(value: 15, label: Text('15')),
                      ButtonSegment(value: 20, label: Text('20 Pro')),
                      ButtonSegment(value: 33, label: Text('33 Pro')),
                    ],
                    selected: const {10},
                    onSelectionChanged: (s) {},
                  ),
                  const SizedBox(height: 12),
                  const TextField(decoration: InputDecoration(labelText: 'Fixas: 01, 05, 10', border: OutlineInputBorder())),
                  const SizedBox(height: 8),
                  const TextField(decoration: InputDecoration(labelText: 'Bloqueadas: 25', border: OutlineInputBorder())),
                ],
              ),
            ),
          ),
          const SizedBox(height: 16),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('🎛️ Filtros', style: Theme.of(context).textTheme.titleLarge),
                  Wrap(
                    spacing: 8,
                    children: [
                      FilterChip(label: const Text('Ímpares'), selected: true, onSelected: (v) {}),
                      FilterChip(label: const Text('Moldura'), selected: false, onSelected: (v) {}),
                      FilterChip(label: const Text('Primos'), selected: false, onSelected: (v) {}),
                      FilterChip(label: const Text('Soma'), selected: false, onSelected: (v) {}),
                      FilterChip(label: const Text('Fibonacci'), selected: false, onSelected: (v) {}),
                      FilterChip(label: const Text('🎯 Cofre Seguro'), selected: false, onSelected: (v) {}),
                    ],
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 16),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                children: [
                  Text('🎚️ Hiperparâmetros', style: Theme.of(context).textTheme.titleLarge),
                  ListTile(title: const Text('Mutação 5%'), subtitle: Slider(value: 5, min: 1, max: 25, onChanged: (v) {})),
                  ListTile(title: const Text('Severidade 80%'), subtitle: Slider(value: 80, min: 0, max: 100, onChanged: (v) {})),
                  SwitchListTile(title: const Text('Memória de Erro'), value: true, onChanged: (v) {}),
                  SwitchListTile(title: const Text('Hamming Diversity'), value: false, onChanged: (v) {}),
                ],
              ),
            ),
          ),
          const SizedBox(height: 24),
          FilledButton.icon(
            onPressed: () {},
            icon: const Icon(Icons.rocket_launch),
            label: const Text('▶️ Iniciar Motor Híbrido'),
            style: FilledButton.styleFrom(minimumSize: const Size.fromHeight(56)),
          ),
        ],
      ),
    );
  }
}

class InteligenciaScreen extends StatelessWidget {
  const InteligenciaScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: 4,
      child: Scaffold(
        appBar: AppBar(
          title: const Text('Inteligência'),
          bottom: const TabBar(tabs: [
            Tab(text: 'Atrasômetro'),
            Tab(text: 'Markov'),
            Tab(text: 'Ensemble'),
            Tab(text: 'Apriori'),
          ]),
        ),
        body: TabBarView(children: [
          _IAList(tipo: 'Atrasômetro', cor: AppColors.primary),
          _IAList(tipo: 'Markov', cor: AppColors.secondary),
          _IAList(tipo: 'Ensemble', cor: AppColors.error, isPro: true),
          _IAList(tipo: 'Apriori', cor: AppColors.tertiary, isPro: true),
        ]),
      ),
    );
  }
}

class _IAList extends StatelessWidget {
  final String tipo;
  final Color cor;
  final bool isPro;
  const _IAList({required this.tipo, required this.cor, this.isPro = false});

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        Card(
          color: cor.withOpacity(0.15),
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              children: [
                Icon(Icons.psychology, color: cor, size: 32),
                const SizedBox(height: 8),
                Text(tipo, style: Theme.of(context).textTheme.titleLarge?.copyWith(color: cor)),
                Text('Análise ${tipo.toLowerCase()} com IA', style: Theme.of(context).textTheme.bodyMedium),
                if (isPro) const Chip(label: Text('PRO'), backgroundColor: AppColors.tertiary),
              ],
            ),
          ),
        ),
        const SizedBox(height: 16),
        ...List.generate(10, (i) => Card(
          child: ListTile(
            leading: CircleAvatar(backgroundColor: cor, child: Text('${i+1}', style: const TextStyle(color: Colors.white))),
            title: Text('Dezena ${(i*2+3)%25+1}'),
            subtitle: Text('Score: ${(95-i*3.5).toStringAsFixed(1)} pts'),
            trailing: IconButton(icon: const Icon(Icons.push_pin), onPressed: () {}),
          ),
        )),
        const SizedBox(height: 16),
        // Heatmap mock
        Card(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              children: [
                Text('🔥 Heatmap 5x5', style: Theme.of(context).textTheme.titleMedium),
                const SizedBox(height: 12),
                GridView.builder(
                  shrinkWrap: true,
                  physics: const NeverScrollableScrollPhysics(),
                  gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(crossAxisCount: 5, mainAxisSpacing: 8, crossAxisSpacing: 8),
                  itemCount: 25,
                  itemBuilder: (c, i) => Container(
                    decoration: BoxDecoration(
                      color: Color.lerp(Colors.blue, Colors.red, i/25)!,
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Center(child: Text('${i+1}', style: const TextStyle(fontWeight: FontWeight.bold))),
                  ),
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }
}

class RankingScreen extends StatelessWidget {
  const RankingScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Ranking Top 50'),
        actions: [IconButton(icon: const Icon(Icons.refresh), onPressed: () {})],
      ),
      body: ListView.builder(
        padding: const EdgeInsets.all(12),
        itemCount: 15,
        itemBuilder: (context, i) => Card(
          child: ListTile(
            leading: CircleAvatar(backgroundColor: i==0? AppColors.tertiary : AppColors.primary, child: Text('${i+1}')),
            title: Text('R\$ ${(1500-i*45.5).toStringAsFixed(2)} • G${42+i}'),
            subtitle: Text('Base: 01 02 05 07 10 11 13 15 18 20...'),
            trailing: const Icon(Icons.chevron_right),
            onTap: () {},
          ),
        ),
      ),
    );
  }
}

class PremiumScreen extends StatelessWidget {
  const PremiumScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Premium')),
      body: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          Card(
            color: AppColors.tertiary.withOpacity(0.15),
            child: Padding(
              padding: const EdgeInsets.all(24),
              child: Column(
                children: [
                  const Icon(Icons.workspace_premium, size: 64, color: AppColors.tertiary),
                  const SizedBox(height: 12),
                  Text('Lotofácil Pro Premium', style: Theme.of(context).textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.bold)),
                  const Text('Desbloqueie o potencial máximo'),
                  const SizedBox(height: 16),
                  const Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text('✅ 33 jogos (vs 10 free)'),
                      Text('✅ IA completa: Ensemble, Apriori, Auto-Piloto, RL'),
                      Text('✅ Gerações ilimitadas'),
                      Text('✅ Sem anúncios'),
                      Text('✅ Export CSV/PDF + WhatsApp sem marca'),
                      Text('✅ Turbo + Snapshots ilimitados'),
                      Text('✅ Suporte prioritário'),
                    ],
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 24),
          FilledButton(
            onPressed: () {},
            style: FilledButton.styleFrom(backgroundColor: AppColors.primary, minimumSize: const Size.fromHeight(56)),
            child: const Text('Anual R\$99 - 58% OFF • 3 dias grátis'),
          ),
          const SizedBox(height: 12),
          FilledButton.tonal(
            onPressed: () {},
            style: FilledButton.styleFrom(minimumSize: const Size.fromHeight(48)),
            child: const Text('Mensal R\$19,90'),
          ),
          const SizedBox(height: 12),
          OutlinedButton(
            onPressed: () {},
            style: OutlinedButton.styleFrom(minimumSize: const Size.fromHeight(48)),
            child: const Text('Vitalício R\$199 - Pagamento único'),
          ),
          const SizedBox(height: 24),
          const Text('Restaura compras • Termos • Privacidade', textAlign: TextAlign.center, style: TextStyle(color: Colors.grey)),
        ],
      ),
    );
  }
}
