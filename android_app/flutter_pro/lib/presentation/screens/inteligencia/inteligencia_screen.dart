import 'package:flutter/material.dart';
import '../../../core/constants/colors.dart';
import '../../widgets/heatmap_widget.dart';
import '../../../data/datasources/local_datasource.dart';

class InteligenciaScreen extends StatefulWidget {
  const InteligenciaScreen({super.key});

  @override
  State<InteligenciaScreen> createState() => _InteligenciaScreenState();
}

class _InteligenciaScreenState extends State<InteligenciaScreen> with SingleTickerProviderStateMixin {
  late TabController _tabController;
  Map<int, double> frequenciaMock = {};
  List<Map<String, dynamic>> dadosAtuais = [];

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 5, vsync: this);
    for (int i = 1; i <= 25; i++) {
      frequenciaMock[i] = (i % 7) / 7 + 0.3;
    }
    _carregarAtrasometro();
    _tabController.addListener(() {
      if (_tabController.indexIsChanging) return;
      switch (_tabController.index) {
        case 0: _carregarAtrasometro(); break;
        case 1: _carregarMarkov(); break;
        case 2: _carregarEnsemble(); break;
        case 3: _carregarApriori(); break;
        case 4: _carregarAutopiloto(); break;
      }
    });
  }

  void _carregarAtrasometro() {
    setState(() {
      dadosAtuais = List.generate(15, (i) => {
        'dezena': (i * 3 + 7) % 25 + 1,
        'atual': 15 - i + (i % 3),
        'media': 4.5 + (i % 4),
        'status': i < 3 ? 'ESTOURANDO' : 'NORMAL',
        'score': 95 - i * 3,
      });
    });
  }

  void _carregarMarkov() {
    setState(() {
      dadosAtuais = List.generate(15, (i) => {
        'dezena': (i * 5 + 2) % 25 + 1,
        'peso': 0.85 - i * 0.05,
        'score': 90 - i * 2,
      });
    });
  }

  void _carregarEnsemble() {
    // Verifica premium
    var isPremium = LocalDataSource().isPremium() as bool? ?? false;
    if (!isPremium) {
      setState(() {
        dadosAtuais = [
          {'pro': true, 'msg': 'Ensemble é Pro! Assine para desbloquear Conselho Jedi com XGBoost'}
        ];
      });
      return;
    }
    setState(() {
      dadosAtuais = List.generate(10, (i) => {
        'dezena': (i * 7 + 1) % 25 + 1,
        'score': 98 - i * 2.5,
      });
    });
  }

  void _carregarApriori() {
    setState(() {
      dadosAtuais = List.generate(10, (i) => {
        'combo': [1 + (i*2) % 25, 5 + (i*3) % 25, 10 + (i*4) % 25],
        'freq': 45 - i * 2,
      });
    });
  }

  void _carregarAutopiloto() {
    setState(() {
      dadosAtuais = [
        {'filtro': 'Ímpares', 'valor': 8, 'desc': 'Previsto 8 ímpares'},
        {'filtro': 'Moldura', 'valor': 10, 'desc': 'Previsto 10 moldura'},
        {'filtro': 'Primos', 'valor': 5, 'desc': 'Previsto 5 primos'},
        {'filtro': 'Soma', 'valor': 198, 'desc': 'Soma prevista 198'},
        {'filtro': 'Fibonacci', 'valor': 5, 'desc': 'Previsto 5 fibonacci'},
      ];
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Inteligência'),
        bottom: TabBar(
          controller: _tabController,
          isScrollable: true,
          tabs: const [
            Tab(text: 'Atrasômetro', icon: Icon(Icons.timer)),
            Tab(text: 'Markov', icon: Icon(Icons.hub)),
            Tab(text: 'Ensemble', icon: Icon(Icons.psychology)),
            Tab(text: 'Apriori', icon: Icon(Icons.diamond)),
            Tab(text: 'Auto-Piloto', icon: Icon(Icons.auto_awesome)),
          ],
        ),
      ),
      body: TabBarView(
        controller: _tabController,
        children: [
          _buildAtrasometroTab(),
          _buildMarkovTab(),
          _buildEnsembleTab(),
          _buildAprioriTab(),
          _buildAutopilotoTab(),
        ],
      ),
    );
  }

  Widget _buildAtrasometroTab() {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        _infoCard(
          icon: Icons.timer,
          color: AppColors.primary,
          title: '⏱️ Atrasômetro Analítico',
          desc: 'Analisa média, variância e desvio padrão de cada dezena. Detecta ruptura 2 sigma - dezenas prestes a estourar.',
        ),
        const SizedBox(height: 16),
        ...dadosAtuais.map((d) => Card(
          child: ListTile(
            leading: CircleAvatar(
              backgroundColor: d['status'] == 'ESTOURANDO' ? AppColors.error : AppColors.primary,
              child: Text('${d['dezena']}', style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
            ),
            title: Text('Dezena ${d['dezena'].toString().padLeft(2, '0')} | Atraso: ${d['atual']}'),
            subtitle: Text('Média: ${d['media']} | ${d['status']}'),
            trailing: IconButton(icon: const Icon(Icons.push_pin), onPressed: () {}),
          ),
        )),
        const SizedBox(height: 16),
        _heatmapCard(),
      ],
    );
  }

  Widget _buildMarkovTab() {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        _infoCard(
          icon: Icons.hub,
          color: AppColors.secondary,
          title: '🔗 Cadeias de Markov',
          desc: 'Probabilidade condicional: Toda vez que bola X sai, bola Y tem Z% de chance de sair depois. Calcula sinergia entre dezenas.',
        ),
        const SizedBox(height: 16),
        ...dadosAtuais.map((d) => Card(
          child: ListTile(
            leading: CircleAvatar(backgroundColor: AppColors.secondary, child: Text('${d['dezena']}')),
            title: Text('Dezena ${d['dezena']} | Peso: ${d['peso'].toStringAsFixed(4)}'),
            subtitle: LinearProgressIndicator(value: d['peso'], color: AppColors.secondary),
            trailing: IconButton(icon: const Icon(Icons.push_pin), onPressed: () {}),
          ),
        )),
      ],
    );
  }

  Widget _buildEnsembleTab() {
    bool isPro = dadosAtuais.isNotEmpty && dadosAtuais.first['pro'] == true;
    if (isPro) {
      return Center(
        child: Padding(
          padding: const EdgeInsets.all(32),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(Icons.lock, size: 64, color: AppColors.tertiary),
              const SizedBox(height: 16),
              Text('Ensemble é Pro', style: Theme.of(context).textTheme.headlineSmall),
              const SizedBox(height: 8),
              Text(dadosAtuais.first['msg'], textAlign: TextAlign.center),
              const SizedBox(height: 24),
              FilledButton.icon(
                onPressed: () {},
                icon: const Icon(Icons.workspace_premium),
                label: const Text('Desbloquear Pro R\$99/ano'),
              ),
            ],
          ),
        ),
      );
    }

    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        _infoCard(
          icon: Icons.psychology,
          color: AppColors.error,
          title: '👑 Ensemble Híbrido (Conselho Jedi)',
          desc: '40% Markov + 20% Atraso + 40% XGBoost. Vota e entrega Top 5 dezenas supremas. Força total!',
        ),
        const SizedBox(height: 16),
        ...dadosAtuais.map((d) => Card(
          color: AppColors.error.withOpacity(0.05),
          child: ListTile(
            leading: CircleAvatar(backgroundColor: AppColors.error, child: Text('${d['dezena']}', style: const TextStyle(color: Colors.white))),
            title: Text('Dezena ${d['dezena']} | ⭐ ${d['score'].toStringAsFixed(1)} pts'),
            subtitle: LinearProgressIndicator(value: d['score']/100, color: AppColors.error),
            trailing: const Icon(Icons.star, color: AppColors.tertiary),
          ),
        )),
      ],
    );
  }

  Widget _buildAprioriTab() {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        _infoCard(
          icon: Icons.diamond,
          color: AppColors.tertiary,
          title: '💎 Mineração Apriori (Combos de Ouro)',
          desc: 'Varre últimos 500 sorteios caçando trincas que sempre saem juntas. Bônus genético para jogos com essas combinações.',
        ),
        const SizedBox(height: 16),
        ...dadosAtuais.map((d) => Card(
          child: ListTile(
            leading: const Icon(Icons.diamond, color: AppColors.tertiary),
            title: Text('Combo: ${d['combo'].map((n) => n.toString().padLeft(2, '0')).join(' - ')}'),
            subtitle: Text('Frequência: ${d['freq']}x nos últimos 500'),
            trailing: Text('${d['freq']}%', style: const TextStyle(fontWeight: FontWeight.bold)),
          ),
        )),
      ],
    );
  }

  Widget _buildAutopilotoTab() {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        _infoCard(
          icon: Icons.auto_awesome,
          color: AppColors.info,
          title: '🎯 Auto-Piloto de Filtros (XGBoost)',
          desc: 'Substitui adivinhação humana. XGBoost Regressor prevê alvos exatos dos filtros para próximo sorteio. Brutal!',
        ),
        const SizedBox(height: 16),
        ...dadosAtuais.map((d) => Card(
          child: ListTile(
            leading: CircleAvatar(backgroundColor: AppColors.info, child: Text('${d['valor']}')),
            title: Text(d['filtro']),
            subtitle: Text(d['desc']),
            trailing: Switch(value: true, onChanged: (_) {}),
          ),
        )),
        const SizedBox(height: 16),
        FilledButton.icon(
          onPressed: () {},
          icon: const Icon(Icons.auto_fix_high),
          label: const Text('Aplicar Auto-Piloto nos Filtros'),
          style: FilledButton.styleFrom(minimumSize: const Size.fromHeight(48)),
        ),
      ],
    );
  }

  Widget _infoCard({required IconData icon, required Color color, required String title, required String desc}) {
    return Card(
      color: color.withOpacity(0.1),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Row(
          children: [
            Icon(icon, color: color, size: 32),
            const SizedBox(width: 16),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(title, style: TextStyle(fontWeight: FontWeight.bold, color: color)),
                  const SizedBox(height: 4),
                  Text(desc, style: const TextStyle(fontSize: 12)),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _heatmapCard() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('🔥 Heatmap Sensorial', style: Theme.of(context).textTheme.titleMedium),
            const SizedBox(height: 12),
            HeatmapWidget(frequencia: frequenciaMock),
            const SizedBox(height: 12),
            const HeatmapLegend(),
          ],
        ),
      ),
    );
  }
}
