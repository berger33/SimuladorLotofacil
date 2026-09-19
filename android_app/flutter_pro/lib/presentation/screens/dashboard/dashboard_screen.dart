import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import '../../../core/constants/colors.dart';
import '../../widgets/heatmap_widget.dart';
import '../../../data/datasources/local_datasource.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  List<double> topScores = [0, 20, 80, 120, 180, 250, 300, 320, 350, 380];
  List<double> mediaScores = [0, -20, 10, 40, 60, 90, 120, 140, 160, 180];
  Map<int, double> frequenciaMock = {};
  List<String> anomalias = [
    "✅ 3675 sorteios carregados",
    "📊 Atrasômetro: Dezena 07 estourando (atraso 18)",
    "🔗 Markov: Forte sinergia 04→22 (80%)",
    "💰 Novo top: R\$ 380 na G9",
  ];
  List<int> ultimoSorteio = [1, 3, 5, 7, 10, 11, 13, 15, 18, 20, 21, 22, 23, 24, 25];

  @override
  void initState() {
    super.initState();
    // Mock frequência para heatmap
    for (int i = 1; i <= 25; i++) {
      frequenciaMock[i] = (i % 5) / 5 + 0.2 + (i / 25) * 0.3;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Dashboard'),
        actions: [
          IconButton(icon: const Icon(Icons.notifications_none), onPressed: () {}),
          IconButton(icon: const Icon(Icons.account_circle), onPressed: () {}),
        ],
      ),
      body: RefreshIndicator(
        onRefresh: () async {
          await Future.delayed(const Duration(seconds: 1));
          setState(() {
            topScores = [...topScores, topScores.last + 20];
          });
        },
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            // Card Top Score com gradiente
            Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                gradient: AppColors.gradientPrimary,
                borderRadius: BorderRadius.circular(20),
                boxShadow: [
                  BoxShadow(color: AppColors.primary.withOpacity(0.3), blurRadius: 12, offset: const Offset(0, 6)),
                ],
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      const Icon(Icons.emoji_events, color: Colors.white70),
                      const SizedBox(width: 8),
                      Text('Top Score', style: Theme.of(context).textTheme.titleMedium?.copyWith(color: Colors.white70)),
                      const Spacer(),
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                        decoration: BoxDecoration(color: Colors.white.withOpacity(0.2), borderRadius: BorderRadius.circular(12)),
                        child: const Text('PRO', style: TextStyle(color: Colors.white, fontSize: 10, fontWeight: FontWeight.bold)),
                      ),
                    ],
                  ),
                  const SizedBox(height: 8),
                  Text('R\$ ${topScores.last.toStringAsFixed(2)}', style: Theme.of(context).textTheme.headlineMedium?.copyWith(color: Colors.white, fontWeight: FontWeight.bold)),
                  const SizedBox(height: 4),
                  Text('Geração ${topScores.length} • Média R\$ ${mediaScores.last.toStringAsFixed(0)} • 3675 sorteios',
                      style: Theme.of(context).textTheme.bodySmall?.copyWith(color: Colors.white70)),
                ],
              ),
            ),
            const SizedBox(height: 16),

            // 3 cards stats
            Row(
              children: [
                Expanded(child: _statCard('Top', 'R\$ ${topScores.last.toStringAsFixed(0)}', Icons.trending_up, AppColors.success)),
                const SizedBox(width: 8),
                Expanded(child: _statCard('Média', 'R\$ ${mediaScores.last.toStringAsFixed(0)}', Icons.show_chart, AppColors.secondary)),
                const SizedBox(width: 8),
                Expanded(child: _statCard('Drawdown', 'R\$ 120', Icons.warning, AppColors.warning)),
              ],
            ),
            const SizedBox(height: 16),

            // Último sorteio
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        const Icon(Icons.calendar_today, size: 18),
                        const SizedBox(width: 8),
                        Text('Último Sorteio • Conc 3500 • 18/09/2026', style: Theme.of(context).textTheme.titleSmall),
                      ],
                    ),
                    const SizedBox(height: 12),
                    Wrap(
                      spacing: 6,
                      runSpacing: 6,
                      children: ultimoSorteio.map((n) => Container(
                        width: 36,
                        height: 36,
                        decoration: BoxDecoration(
                          color: AppColors.primary,
                          borderRadius: BorderRadius.circular(18),
                        ),
                        child: Center(
                          child: Text(
                            n.toString().padLeft(2, '0'),
                            style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 13),
                          ),
                        ),
                      )).toList(),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 16),

            // Gráfico convergência
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        const Icon(Icons.show_chart, color: AppColors.success),
                        const SizedBox(width: 8),
                        Text('Convergência (ECG)', style: Theme.of(context).textTheme.titleMedium),
                        const Spacer(),
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                          decoration: BoxDecoration(color: AppColors.success.withOpacity(0.15), borderRadius: BorderRadius.circular(8)),
                          child: Text('Top ↑', style: TextStyle(color: AppColors.success, fontSize: 12, fontWeight: FontWeight.bold)),
                        ),
                      ],
                    ),
                    const SizedBox(height: 16),
                    SizedBox(
                      height: 200,
                      child: LineChart(
                        LineChartData(
                          gridData: FlGridData(show: true, drawVerticalLine: false),
                          titlesData: FlTitlesData(
                            leftTitles: AxisTitles(sideTitles: SideTitles(showTitles: true, reservedSize: 40)),
                            bottomTitles: AxisTitles(sideTitles: SideTitles(showTitles: true, reservedSize: 22)),
                            rightTitles: AxisTitles(sideTitles: SideTitles(showTitles: false)),
                            topTitles: AxisTitles(sideTitles: SideTitles(showTitles: false)),
                          ),
                          borderData: FlBorderData(show: false),
                          lineBarsData: [
                            LineChartBarData(
                              spots: List.generate(topScores.length, (i) => FlSpot(i.toDouble(), topScores[i])),
                              isCurved: true,
                              color: AppColors.success,
                              barWidth: 3,
                              dotData: FlDotData(show: false),
                              belowBarData: BarAreaData(show: true, color: AppColors.success.withOpacity(0.15)),
                            ),
                            LineChartBarData(
                              spots: List.generate(mediaScores.length, (i) => FlSpot(i.toDouble(), mediaScores[i])),
                              isCurved: true,
                              color: AppColors.secondary,
                              barWidth: 2,
                              dotData: FlDotData(show: false),
                              dashArray: [5, 5],
                            ),
                          ],
                        ),
                      ),
                    ),
                    const SizedBox(height: 8),
                    Row(
                      children: [
                        _legendDot(AppColors.success, 'Top 1'),
                        const SizedBox(width: 16),
                        _legendDot(AppColors.secondary, 'Média Pop'),
                      ],
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 16),

            // Anomalias
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        const Icon(Icons.warning_amber, color: AppColors.tertiary),
                        const SizedBox(width: 8),
                        Text('Caçador de Anomalias', style: Theme.of(context).textTheme.titleMedium),
                      ],
                    ),
                    const SizedBox(height: 12),
                    ...anomalias.map((a) => Padding(
                      padding: const EdgeInsets.only(bottom: 8),
                      child: Row(
                        children: [
                          const Text('• ', style: TextStyle(fontWeight: FontWeight.bold)),
                          Expanded(child: Text(a, style: Theme.of(context).textTheme.bodySmall)),
                        ],
                      ),
                    )),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 16),

            // Heatmap preview
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text('🔥 Heatmap Sensorial', style: Theme.of(context).textTheme.titleMedium),
                    const SizedBox(height: 12),
                    HeatmapWidget(frequencia: frequenciaMock, onTapDezena: (d) {
                      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Dezena $d selecionada')));
                    }),
                    const SizedBox(height: 12),
                    const HeatmapLegend(),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 16),

            // Atalhos
            Row(
              children: [
                Expanded(child: _actionButton('Gerar', Icons.auto_fix_high, AppColors.primary, () {})),
                const SizedBox(width: 8),
                Expanded(child: _actionButton('IA', Icons.psychology, AppColors.secondary, () {})),
                const SizedBox(width: 8),
                Expanded(child: _actionButton('Ranking', Icons.emoji_events, AppColors.tertiary, () {})),
              ],
            ),
            const SizedBox(height: 16),

            // Banner Ad placeholder
            Container(
              height: 60,
              decoration: BoxDecoration(
                color: Colors.grey[800],
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: Colors.grey[700]!),
              ),
              child: const Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(Icons.ad_units, color: Colors.white54, size: 20),
                    Text('AdMob Banner (Free) - R\$ 0.20 eCPM', style: TextStyle(color: Colors.white54, fontSize: 11)),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 80),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () {},
        icon: const Icon(Icons.rocket_launch),
        label: const Text('Gerar Matriz'),
        backgroundColor: AppColors.primary,
      ),
    );
  }

  Widget _statCard(String label, String value, IconData icon, Color color) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(
          children: [
            Icon(icon, color: color, size: 20),
            const SizedBox(height: 4),
            Text(label, style: const TextStyle(fontSize: 11, color: Colors.grey)),
            Text(value, style: TextStyle(fontSize: 14, fontWeight: FontWeight.bold, color: color)),
          ],
        ),
      ),
    );
  }

  Widget _legendDot(Color color, String label) {
    return Row(
      children: [
        Container(width: 12, height: 3, color: color),
        const SizedBox(width: 4),
        Text(label, style: const TextStyle(fontSize: 11)),
      ],
    );
  }

  Widget _actionButton(String label, IconData icon, Color color, VoidCallback onTap) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(12),
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 16),
        decoration: BoxDecoration(
          color: color.withOpacity(0.15),
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: color.withOpacity(0.3)),
        ),
        child: Column(
          children: [
            Icon(icon, color: color),
            const SizedBox(height: 4),
            Text(label, style: TextStyle(color: color, fontWeight: FontWeight.bold, fontSize: 12)),
          ],
        ),
      ),
    );
  }
}
