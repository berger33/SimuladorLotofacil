import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import '../../../core/constants/colors.dart';
import '../../widgets/heatmap_widget.dart';

/// Dashboard 100% idêntico ao screenshot 01_dashboard.webp
/// Design System: #0A0A0F bg, #1A1D29 card, #7C3AED primary, gradiente Top Score
class DashboardPixelPerfect extends StatefulWidget {
  const DashboardPixelPerfect({super.key});

  @override
  State<DashboardPixelPerfect> createState() => _DashboardPixelPerfectState();
}

class _DashboardPixelPerfectState extends State<DashboardPixelPerfect> {
  double topScore = 1234.56;
  int geracaoAtual = 42;
  List<double> topScores = [500, 600, 750, 850, 800, 900, 880, 920, 1100, 1200, 1300, 1450, 1400, 1480, 1470];
  List<double> mediaScores = [250, 300, 350, 400, 380, 420, 400, 450, 480, 500, 520, 580, 600, 620, 650];
  List<int> ultimoSorteio = [1, 3, 5, 7, 10, 11, 13, 15, 18, 20, 21, 22, 23, 24, 25];
  Map<int, double> frequencia = {};

  @override
  void initState() {
    super.initState();
    for (int i = 1; i <= 25; i++) {
      frequencia[i] = (i % 5) / 5 + 0.2 + (i / 25) * 0.3 + (i == 5 || i == 8 || i == 13 || i == 18 || i == 25 ? 0.4 : 0);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        backgroundColor: AppColors.background,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.menu, color: Colors.white),
          onPressed: () {},
        ),
        title: RichText(
          text: const TextSpan(
            children: [
              TextSpan(text: 'Lotofácil ', style: TextStyle(color: Colors.white, fontWeight: FontWeight.w700, fontSize: 18)),
              TextSpan(text: 'Pro', style: TextStyle(color: Color(0xFF8B5CF6), fontWeight: FontWeight.w700, fontSize: 18)),
            ],
          ),
        ),
        actions: [
          Stack(
            children: [
              IconButton(icon: const Icon(Icons.notifications_none, color: Colors.white70), onPressed: () {}),
              Positioned(
                right: 12, top: 12,
                child: Container(width: 8, height: 8, decoration: const BoxDecoration(color: Color(0xFF8B5CF6), shape: BoxShape.circle)),
              ),
            ],
          ),
        ],
      ),
      body: ListView(
        padding: const EdgeInsets.fromLTRB(16, 8, 16, 100),
        children: [
          // TOP SCORE CARD - Gradiente idêntico screenshot
          Container(
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              gradient: AppColors.gradientTopScore,
              borderRadius: BorderRadius.circular(20),
              boxShadow: [BoxShadow(color: AppColors.primary.withOpacity(0.3), blurRadius: 20, offset: const Offset(0, 8))],
            ),
            child: Row(
              children: [
                Container(
                  width: 56, height: 56,
                  decoration: BoxDecoration(color: Colors.white.withOpacity(0.15), shape: BoxShape.circle),
                  child: const Icon(Icons.emoji_events, color: Colors.white, size: 28),
                ),
                const SizedBox(width: 14),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text('TOP SCORE', style: TextStyle(color: Colors.white70, fontSize: 11, fontWeight: FontWeight.w600, letterSpacing: 1)),
                      const SizedBox(height: 2),
                      Text('R\$ ${topScore.toStringAsFixed(2).replaceAll('.', ',')}', style: const TextStyle(color: Colors.white, fontSize: 24, fontWeight: FontWeight.w800)),
                      const SizedBox(height: 4),
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                        decoration: BoxDecoration(color: const Color(0xFF8B5CF6).withOpacity(0.3), borderRadius: BorderRadius.circular(12), border: Border.all(color: const Color(0xFF8B5CF6).withOpacity(0.5))),
                        child: const Text('Melhor resultado', style: TextStyle(color: Color(0xFFC4B5FD), fontSize: 10, fontWeight: FontWeight.w600)),
                      ),
                    ],
                  ),
                ),
                Container(width: 1, height: 60, color: Colors.white.withOpacity(0.15)),
                const SizedBox(width: 20),
                Column(
                  crossAxisAlignment: CrossAxisAlignment.end,
                  children: [
                    const Text('GERAÇÃO ATUAL', style: TextStyle(color: Colors.white60, fontSize: 11, letterSpacing: 0.5)),
                    Text('$geracaoAtual', style: const TextStyle(color: Colors.white, fontSize: 28, fontWeight: FontWeight.w800)),
                    const SizedBox(height: 4),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                      decoration: BoxDecoration(color: const Color(0xFF8B5CF6).withOpacity(0.4), borderRadius: BorderRadius.circular(10)),
                      child: const Text('Em andamento', style: TextStyle(color: Color(0xFFDDD6FE), fontSize: 10, fontWeight: FontWeight.w600)),
                    ),
                  ],
                ),
              ],
            ),
          ),
          const SizedBox(height: 16),

          // CONVERGÊNCIA (MÉDIA x TOP SCORE) - idêntico
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(color: AppColors.surfaceDark, borderRadius: BorderRadius.circular(16), border: Border.all(color: AppColors.border)),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    const Text('CONVERGÊNCIA (MÉDIA × TOP SCORE)', style: TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.w700, letterSpacing: 0.5)),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                      decoration: BoxDecoration(color: AppColors.surface2, borderRadius: BorderRadius.circular(8), border: Border.all(color: AppColors.border)),
                      child: const Row(children: [Text('Últimas 50 gerações', style: TextStyle(color: Color(0xFF9CA3AF), fontSize: 11)), Icon(Icons.keyboard_arrow_down, size: 14, color: Color(0xFF9CA3AF))]),
                    ),
                  ],
                ),
                const SizedBox(height: 12),
                SizedBox(
                  height: 160,
                  child: LineChart(
                    LineChartData(
                      gridData: FlGridData(show: true, drawVerticalLine: false, horizontalInterval: 500, getDrawingHorizontalLine: (v) => FlLine(color: Colors.white.withOpacity(0.06), strokeWidth: 1)),
                      titlesData: FlTitlesData(
                        leftTitles: AxisTitles(sideTitles: SideTitles(showTitles: true, reservedSize: 32, getTitlesWidget: (v, m) => Text('${v.toInt()}', style: const TextStyle(color: Color(0xFF6B7280), fontSize: 10)))),
                        bottomTitles: AxisTitles(sideTitles: SideTitles(showTitles: true, reservedSize: 20, getTitlesWidget: (v, m) {
                          const labels = ['-50', '-40', '-30', '-20', '-10', '0'];
                          final idx = v.toInt();
                          if (idx >= 0 && idx < labels.length) return Text(labels[idx], style: const TextStyle(color: Color(0xFF6B7280), fontSize: 10));
                          return const Text('');
                        }, interval: 1)),
                        rightTitles: AxisTitles(sideTitles: SideTitles(showTitles: false)),
                        topTitles: AxisTitles(sideTitles: SideTitles(showTitles: false)),
                      ),
                      borderData: FlBorderData(show: false),
                      minX: 0, maxX: 14, minY: 0, maxY: 1600,
                      lineBarsData: [
                        LineChartBarData(
                          spots: List.generate(topScores.length, (i) => FlSpot(i.toDouble(), topScores[i])),
                          isCurved: true, color: AppColors.successLight, barWidth: 2, dotData: FlDotData(show: false),
                          belowBarData: BarAreaData(show: true, color: AppColors.successLight.withOpacity(0.1)),
                        ),
                        LineChartBarData(
                          spots: List.generate(mediaScores.length, (i) => FlSpot(i.toDouble(), mediaScores[i])),
                          isCurved: true, color: AppColors.blue, barWidth: 2, dotData: FlDotData(show: false),
                        ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 8),
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    _legendDot(AppColors.successLight, 'Top Score'),
                    const SizedBox(width: 20),
                    _legendDot(AppColors.blue, 'Média'),
                  ],
                ),
              ],
            ),
          ),
          const SizedBox(height: 12),

          // 4 STATS CARDS
          GridView.count(
            crossAxisCount: 2,
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            mainAxisSpacing: 10, crossAxisSpacing: 10, childAspectRatio: 1.6,
            children: [
              _statCard('MÉDIA GERAL', '612,43', 'Últimas 50', Icons.my_location, AppColors.primary, AppColors.primaryLight),
              _statCard('EVOLUÇÃO', '+18,62%', 'vs. 50 anteriores', Icons.trending_up, AppColors.success, AppColors.successLight, isGreen: true),
              _statCard('MÁXIMO', '1.234,56', 'Geração 41', Icons.local_fire_department, AppColors.error, AppColors.primaryLight),
              _statCard('CONVERGÊNCIA', '2,02x', 'Top / Média', Icons.bar_chart, AppColors.blue, AppColors.secondaryLight),
            ],
          ),
          const SizedBox(height: 12),

          // ÚLTIMO CONCURSO
          Container(
            padding: const EdgeInsets.all(14),
            decoration: BoxDecoration(color: AppColors.surfaceDark, borderRadius: BorderRadius.circular(14), border: Border.all(color: AppColors.border)),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    const Text('ÚLTIMO CONCURSO', style: TextStyle(color: Colors.white, fontSize: 11, fontWeight: FontWeight.w700, letterSpacing: 0.5)),
                    Row(children: [Text('Concurso 3134', style: TextStyle(color: AppColors.textSecondary, fontSize: 10)), const SizedBox(width: 12), Text('18/05/2025', style: TextStyle(color: AppColors.textSecondary, fontSize: 10)), const SizedBox(width: 6), const Icon(Icons.calendar_today, size: 14, color: Color(0xFF6B7280))]),
                  ],
                ),
                const SizedBox(height: 12),
                Wrap(
                  spacing: 6, runSpacing: 6,
                  children: ultimoSorteio.map((n) => Container(
                    width: 28, height: 28,
                    decoration: BoxDecoration(color: AppColors.primaryDark, borderRadius: BorderRadius.circular(14), border: Border.all(color: AppColors.primary)),
                    child: Center(child: Text(n.toString().padLeft(2, '0'), style: const TextStyle(color: Colors.white, fontSize: 11, fontWeight: FontWeight.w700))),
                  )).toList(),
                ),
              ],
            ),
          ),
          const SizedBox(height: 12),

          // ANOMALIAS DETECTADAS
          Container(
            padding: const EdgeInsets.all(14),
            decoration: BoxDecoration(color: AppColors.surfaceDark, borderRadius: BorderRadius.circular(14), border: Border.all(color: AppColors.border)),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text('ANOMALIAS DETECTADAS', style: TextStyle(color: Colors.white, fontSize: 11, fontWeight: FontWeight.w700, letterSpacing: 0.5)),
                const SizedBox(height: 12),
                _anomaliaRow('⚠️', 'Intervalo longo sem: 02, 04, 06', 'Há 28 concursos', 'ALTA', AppColors.error),
                const SizedBox(height: 8),
                _anomaliaRow('🕒', 'Números em atraso: 02, 04, 06, 09, 14', 'Acima de 20 concursos', 'MÉDIA', AppColors.warning),
                const SizedBox(height: 8),
                _anomaliaRow('ℹ️', 'Sequência rara detectada: 11, 12, 13', 'Rara nos últimos 100 concursos', 'BAIXA', AppColors.info),
              ],
            ),
          ),
          const SizedBox(height: 12),

          // MAPA DE CALOR
          Container(
            padding: const EdgeInsets.all(14),
            decoration: BoxDecoration(color: AppColors.surfaceDark, borderRadius: BorderRadius.circular(14), border: Border.all(color: AppColors.border)),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    const Text('MAPA DE CALOR – FREQUÊNCIA (ÚLTIMOS 50 CONCURSOS)', style: TextStyle(color: Colors.white, fontSize: 11, fontWeight: FontWeight.w700)),
                    Container(width: 18, height: 18, decoration: BoxDecoration(border: Border.all(color: AppColors.border), shape: BoxShape.circle), child: const Center(child: Text('ⓘ', style: TextStyle(fontSize: 10)))),
                  ],
                ),
                const SizedBox(height: 12),
                Row(
                  children: [
                    Expanded(
                      child: GridView.builder(
                        shrinkWrap: true, physics: const NeverScrollableScrollPhysics(),
                        gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(crossAxisCount: 5, mainAxisSpacing: 6, crossAxisSpacing: 6, childAspectRatio: 1.8),
                        itemCount: 25,
                        itemBuilder: (c, i) {
                          final n = i + 1;
                          final freq = frequencia[n] ?? 0.5;
                          Color color;
                          if (freq < 0.4) color = AppColors.heatFria;
                          else if (freq < 0.6) color = const Color(0xFF2563EB);
                          else if (freq < 0.8) color = AppColors.heatQuente;
                          else color = AppColors.heatMuitoQuente;
                          if ([5, 8, 13, 18, 25].contains(n)) color = AppColors.heatMuitoQuente;
                          else if ([8, 13, 18].contains(n)) color = AppColors.heatQuente;
                          return Container(
                            decoration: BoxDecoration(color: color, borderRadius: BorderRadius.circular(8)),
                            child: Center(child: Text(n.toString().padLeft(2, '0'), style: const TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.w700))),
                          );
                        },
                      ),
                    ),
                    const SizedBox(width: 10),
                    Column(
                      children: [
                        Container(width: 8, height: 60, decoration: BoxDecoration(gradient: const LinearGradient(colors: [Color(0xFF1E3A8A), Color(0xFF3B82F6), Color(0xFFFB923C), Color(0xFFEF4444)], begin: Alignment.topCenter, end: Alignment.bottomCenter), borderRadius: BorderRadius.circular(4))),
                        const SizedBox(height: 6),
                        const Text('Menor\nfrequência', style: TextStyle(color: Color(0xFF9CA3AF), fontSize: 8), textAlign: TextAlign.center),
                        const SizedBox(height: 20),
                        const Text('Maior\nfrequência', style: TextStyle(color: Color(0xFF9CA3AF), fontSize: 8), textAlign: TextAlign.center),
                      ],
                    ),
                  ],
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _legendDot(Color color, String label) {
    return Row(children: [Container(width: 18, height: 3, decoration: BoxDecoration(color: color, borderRadius: BorderRadius.circular(2))), const SizedBox(width: 6), Text(label, style: const TextStyle(color: Color(0xFF9CA3AF), fontSize: 11))]);
  }

  Widget _statCard(String title, String value, String sub, IconData icon, Color iconBg, Color iconColor, {bool isGreen = false}) {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(color: AppColors.surfaceDark, borderRadius: BorderRadius.circular(12), border: Border.all(color: AppColors.border)),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(children: [Container(width: 22, height: 22, decoration: BoxDecoration(color: iconBg.withOpacity(0.2), borderRadius: BorderRadius.circular(6)), child: Icon(icon, size: 12, color: iconColor)), const SizedBox(width: 6), Text(title, style: const TextStyle(color: Color(0xFF9CA3AF), fontSize: 9, fontWeight: FontWeight.w600))]),
          const SizedBox(height: 8),
          Text(value, style: TextStyle(color: isGreen ? AppColors.successLight : Colors.white, fontSize: 16, fontWeight: FontWeight.w700)),
          const SizedBox(height: 2),
          Text(sub, style: TextStyle(color: isGreen ? Colors.white70 : (title == 'MÁXIMO' ? AppColors.primaryLight : (title == 'CONVERGÊNCIA' ? AppColors.secondaryLight : AppColors.primaryLight)), fontSize: 10)),
        ],
      ),
    );
  }

  Widget _anomaliaRow(String icon, String title, String desc, String badge, Color badgeColor) {
    return Container(
      padding: const EdgeInsets.all(10),
      decoration: BoxDecoration(color: AppColors.surface2, borderRadius: BorderRadius.circular(10), border: Border.all(color: AppColors.border)),
      child: Row(
        children: [
          Container(width: 28, height: 28, decoration: BoxDecoration(color: badgeColor.withOpacity(0.15), shape: BoxShape.circle), child: Center(child: Text(icon, style: const TextStyle(fontSize: 14)))),
          const SizedBox(width: 10),
          Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [Text(title, style: const TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.w500)), const SizedBox(height: 2), Text(desc, style: const TextStyle(color: Color(0xFF9CA3AF), fontSize: 10))])),
          Container(padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4), decoration: BoxDecoration(color: badgeColor.withOpacity(0.1), borderRadius: BorderRadius.circular(12), border: Border.all(color: badgeColor)), child: Text(badge, style: TextStyle(color: badgeColor, fontSize: 9, fontWeight: FontWeight.w700))),
        ],
      ),
    );
  }
}
