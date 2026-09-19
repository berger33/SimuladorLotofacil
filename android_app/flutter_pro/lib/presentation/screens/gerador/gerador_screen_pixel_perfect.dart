import 'package:flutter/material.dart';
import '../../../core/constants/colors.dart';

/// Gerador 100% idêntico ao screenshot 02_gerador.webp
class GeradorPixelPerfect extends StatefulWidget {
  const GeradorPixelPerfect({super.key});

  @override
  State<GeradorPixelPerfect> createState() => _GeradorPixelPerfectState();
}

class _GeradorPixelPerfectState extends State<GeradorPixelPerfect> {
  int qtdJogos = 33;
  List<int> fixas = [1, 5, 10];
  List<int> bloqueadas = [25];
  Set<String> filtrosAtivos = {'Impares', 'Moldura', 'Primos', 'Foco 14'};
  double mutacao = 5;
  double severidade = 80;
  bool memoriaErro = true;
  bool hamming = true;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        backgroundColor: AppColors.background,
        elevation: 0,
        leading: IconButton(icon: const Icon(Icons.menu, color: Colors.white), onPressed: () {}),
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            RichText(text: const TextSpan(children: [
              TextSpan(text: 'Lotofácil ', style: TextStyle(color: Colors.white, fontWeight: FontWeight.w800, fontSize: 18)),
              TextSpan(text: 'PRO', style: TextStyle(color: Color(0xFF8B5CF6), fontWeight: FontWeight.w800, fontSize: 18)),
            ])),
            const Text('Generator', style: TextStyle(color: Color(0xFF9CA3AF), fontSize: 12, fontWeight: FontWeight.w400)),
          ],
        ),
        actions: [
          Container(
            margin: const EdgeInsets.only(right: 16),
            width: 36, height: 36,
            decoration: BoxDecoration(color: AppColors.surfaceDark, borderRadius: BorderRadius.circular(10), border: Border.all(color: AppColors.border)),
            child: const Icon(Icons.description_outlined, color: Color(0xFF8B5CF6), size: 20),
          ),
        ],
      ),
      body: ListView(
        padding: const EdgeInsets.fromLTRB(16, 8, 16, 100),
        children: [
          // CONFIGURAÇÕES DO GERADOR
          _sectionCard(
            icon: '⚙️',
            title: 'CONFIGURAÇÕES DO GERADOR',
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text('Qtd Jogos', style: TextStyle(color: Colors.white, fontSize: 14, fontWeight: FontWeight.w600)),
                const SizedBox(height: 10),
                Container(
                  decoration: BoxDecoration(color: AppColors.background2, borderRadius: BorderRadius.circular(12), border: Border.all(color: AppColors.border)),
                  child: Row(
                    children: [
                      _segBtn('10', 'Free', qtdJogos == 10, () => setState(() => qtdJogos = 10)),
                      _segBtn('15', '', qtdJogos == 15, () => setState(() => qtdJogos = 15)),
                      _segBtn('20', '', qtdJogos == 20, () => setState(() => qtdJogos = 20)),
                      _segBtn('33', 'Pro', qtdJogos == 33, () => setState(() => qtdJogos = 33), isPro: true),
                    ],
                  ),
                ),
              ],
            ),
          ),

          // ENGENHARIA GENÉTICA
          _sectionCard(
            icon: '🧬',
            title: 'ENGENHARIA GENÉTICA',
            child: Row(
              children: [
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(children: [const Text('Números Fixos', style: TextStyle(color: Color(0xFF9CA3AF), fontSize: 12)), const SizedBox(width: 6), Container(width: 16, height: 16, decoration: BoxDecoration(border: Border.all(color: AppColors.border), shape: BoxShape.circle), child: const Center(child: Text('ⓘ', style: TextStyle(fontSize: 8))))]),
                      const SizedBox(height: 8),
                      Wrap(spacing: 6, children: fixas.map((n) => _chipFixa(n)).toList()),
                    ],
                  ),
                ),
                Container(width: 1, height: 50, color: AppColors.border, margin: const EdgeInsets.symmetric(horizontal: 12)),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(children: [const Text('Números Bloqueados', style: TextStyle(color: Color(0xFF9CA3AF), fontSize: 12)), const SizedBox(width: 6), Container(width: 16, height: 16, decoration: BoxDecoration(border: Border.all(color: AppColors.border), shape: BoxShape.circle), child: const Center(child: Text('ⓘ', style: TextStyle(fontSize: 8))))]),
                      const SizedBox(height: 8),
                      Wrap(spacing: 6, children: bloqueadas.map((n) => _chipBloq(n)).toList()),
                    ],
                  ),
                ),
              ],
            ),
          ),

          // FILTROS INTELIGENTES
          _sectionCard(
            icon: '🔽',
            title: 'FILTROS INTELIGENTES',
            trailing: Container(padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4), decoration: BoxDecoration(color: AppColors.primary.withOpacity(0.15), borderRadius: BorderRadius.circular(10), border: Border.all(color: AppColors.primary)), child: Text('${filtrosAtivos.length} ativos', style: const TextStyle(color: Color(0xFF8B5CF6), fontSize: 10, fontWeight: FontWeight.w600))),
            child: Wrap(
              spacing: 8, runSpacing: 8,
              children: [
                _filtroChip('Impares', true),
                _filtroChip('Moldura', true),
                _filtroChip('Primos', true),
                _filtroChip('Foco 14', true),
              ],
            ),
          ),

          // CONTROLE EVOLUTIVO
          _sectionCard(
            icon: '🎛️',
            title: 'CONTROLE EVOLUTIVO',
            child: Column(
              children: [
                _sliderRow('Mutação', 'ⓘ', '${mutacao.toInt()}%', mutacao, 1, 25, (v) => setState(() => mutacao = v)),
                const SizedBox(height: 16),
                _sliderRow('Severidade', 'ⓘ', '${severidade.toInt()}%', severidade, 0, 100, (v) => setState(() => severidade = v)),
              ],
            ),
          ),

          // MEMÓRIA E DIVERSIDADE
          _sectionCard(
            icon: '🧠',
            title: 'MEMÓRIA E DIVERSIDADE',
            child: Row(
              children: [
                Expanded(child: _toggleRow('Memória de Erro', 'ⓘ', memoriaErro, (v) => setState(() => memoriaErro = v))),
                Container(width: 1, height: 30, color: AppColors.border, margin: const EdgeInsets.symmetric(horizontal: 12)),
                Expanded(child: _toggleRow('Distância de Hamming', 'ⓘ', hamming, (v) => setState(() => hamming = v))),
              ],
            ),
          ),

          // ESTRATÉGIAS DE BUSCA
          _sectionCard(
            icon: '🎯',
            title: 'ESTRATÉGIAS DE BUSCA',
            child: Column(
              children: [
                _estrategiaRow('🛡️', 'Conservador', 'Prioriza estabilidade e menor variação.'),
                _estrategiaRow('⚡', 'Agressivo', 'Explora mais combinações e padrões.'),
                _estrategiaRow('🤖', 'Robo', 'Equilíbrio entre exploração e precisão.'),
                _estrategiaRow('🛋️', 'Preguiçoso', 'Busca eficiente com menos iterações.', isLast: true),
              ],
            ),
          ),

          // MATERIAL DISPONÍVEL
          Container(
            padding: const EdgeInsets.all(14),
            decoration: BoxDecoration(color: AppColors.surfaceDark, borderRadius: BorderRadius.circular(14), border: Border.all(color: AppColors.border)),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Row(children: [Text('📦', style: TextStyle(fontSize: 16)), SizedBox(width: 8), Text('MATERIAL DISPONÍVEL', style: TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.w600))]),
                Container(padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 6), decoration: BoxDecoration(color: AppColors.primary, borderRadius: BorderRadius.circular(8)), child: const Text('3', style: TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.w700))),
              ],
            ),
          ),
          const SizedBox(height: 16),

          // BOTÃO INICIAR MOTOR HÍBRIDO
          Container(
            width: double.infinity,
            height: 56,
            decoration: BoxDecoration(gradient: LinearGradient(colors: [AppColors.primary, AppColors.primaryDark]), borderRadius: BorderRadius.circular(14), boxShadow: [BoxShadow(color: AppColors.primary.withOpacity(0.3), blurRadius: 20, offset: const Offset(0, 8))]),
            child: const Row(mainAxisAlignment: MainAxisAlignment.center, children: [Text('🚀', style: TextStyle(fontSize: 20)), SizedBox(width: 10), Text('INICIAR MOTOR HÍBRIDO', style: TextStyle(color: Colors.white, fontSize: 14, fontWeight: FontWeight.w800, letterSpacing: 0.5))]),
          ),
        ],
      ),
    );
  }

  Widget _sectionCard({required String icon, required String title, required Widget child, Widget? trailing}) {
    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(color: AppColors.surfaceDark, borderRadius: BorderRadius.circular(14), border: Border.all(color: AppColors.border)),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(children: [Text(icon, style: const TextStyle(fontSize: 14)), const SizedBox(width: 6), Text(title, style: const TextStyle(color: Color(0xFF8B5CF6), fontSize: 11, fontWeight: FontWeight.w700, letterSpacing: 0.8)), const Spacer(), if (trailing != null) trailing]),
          const SizedBox(height: 12),
          child,
        ],
      ),
    );
  }

  Widget _segBtn(String n, String label, bool active, VoidCallback onTap, {bool isPro = false}) {
    return Expanded(
      child: GestureDetector(
        onTap: onTap,
        child: Container(
          padding: const EdgeInsets.symmetric(vertical: 10),
          decoration: BoxDecoration(color: active ? AppColors.primary : Colors.transparent, borderRadius: BorderRadius.circular(10)),
          child: Column(children: [Text(n, style: TextStyle(color: active ? Colors.white : Colors.white, fontSize: 14, fontWeight: FontWeight.w700)), if (label.isNotEmpty) Text(label, style: TextStyle(color: active ? Colors.white : const Color(0xFF9CA3AF), fontSize: 10))]),
        ),
      ),
    );
  }

  Widget _chipFixa(int n) {
    return Container(
      width: 32, height: 32,
      decoration: BoxDecoration(color: const Color(0xFF065F46), borderRadius: BorderRadius.circular(16), border: Border.all(color: const Color(0xFF10B981))),
      child: Center(child: Text(n.toString().padLeft(2, '0'), style: const TextStyle(color: Color(0xFF6EE7B7), fontSize: 12, fontWeight: FontWeight.w700))),
    );
  }

  Widget _chipBloq(int n) {
    return Container(
      width: 32, height: 32,
      decoration: BoxDecoration(color: const Color(0xFF7F1D1D), borderRadius: BorderRadius.circular(16), border: Border.all(color: const Color(0xFFEF4444))),
      child: Center(child: Text(n.toString().padLeft(2, '0'), style: const TextStyle(color: Color(0xFFFCA5A5), fontSize: 12, fontWeight: FontWeight.w700))),
    );
  }

  Widget _filtroChip(String label, bool active) {
    final isActive = filtrosAtivos.contains(label);
    return GestureDetector(
      onTap: () => setState(() => isActive ? filtrosAtivos.remove(label) : filtrosAtivos.add(label)),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
        decoration: BoxDecoration(color: isActive ? AppColors.primary.withOpacity(0.1) : Colors.transparent, borderRadius: BorderRadius.circular(20), border: Border.all(color: isActive ? AppColors.primary : AppColors.border)),
        child: Row(mainAxisSize: MainAxisSize.min, children: [if (isActive) Container(width: 14, height: 14, decoration: const BoxDecoration(color: Color(0xFF7C3AED), shape: BoxShape.circle), child: const Center(child: Text('✓', style: TextStyle(color: Colors.white, fontSize: 8)))) , if (isActive) const SizedBox(width: 6), Text(label, style: TextStyle(color: isActive ? const Color(0xFF8B5CF6) : const Color(0xFF9CA3AF), fontSize: 12, fontWeight: FontWeight.w600))]),
      ),
    );
  }

  Widget _sliderRow(String label, String info, String value, double current, double min, double max, Function(double) onChanged) {
    return Column(
      children: [
        Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [Row(children: [Text(label, style: const TextStyle(color: Colors.white, fontSize: 13)), const SizedBox(width: 6), Container(width: 14, height: 14, decoration: BoxDecoration(border: Border.all(color: AppColors.border), shape: BoxShape.circle), child: Center(child: Text(info, style: const TextStyle(fontSize: 8))))]), Text(value, style: const TextStyle(color: Color(0xFF9CA3AF), fontSize: 12, fontWeight: FontWeight.w600))]),
        const SizedBox(height: 8),
        SliderTheme(
          data: SliderThemeData(trackHeight: 6, thumbShape: const RoundSliderThumbShape(enabledThumbRadius: 9), overlayShape: SliderComponentShape.noOverlay, activeTrackColor: AppColors.primary, inactiveTrackColor: AppColors.border, thumbColor: Colors.white),
          child: Slider(value: current, min: min, max: max, onChanged: onChanged),
        ),
      ],
    );
  }

  Widget _toggleRow(String label, String info, bool value, Function(bool) onChanged) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Expanded(child: Row(children: [Flexible(child: Text(label, style: const TextStyle(color: Colors.white, fontSize: 11))), const SizedBox(width: 4), Container(width: 12, height: 12, decoration: BoxDecoration(border: Border.all(color: AppColors.border), shape: BoxShape.circle), child: Center(child: Text(info, style: const TextStyle(fontSize: 6))))])),
        const SizedBox(width: 8),
        GestureDetector(
          onTap: () => onChanged(!value),
          child: Container(width: 44, height: 26, decoration: BoxDecoration(color: value ? AppColors.primary : AppColors.border, borderRadius: BorderRadius.circular(13)), child: Stack(children: [AnimatedPositioned(duration: const Duration(milliseconds: 200), left: value ? 21 : 3, top: 3, child: Container(width: 20, height: 20, decoration: const BoxDecoration(color: Colors.white, shape: BoxShape.circle, boxShadow: [BoxShadow(color: Colors.black26, blurRadius: 3)])))])),
        ),
      ],
    );
  }

  Widget _estrategiaRow(String icon, String title, String desc, {bool isLast = false}) {
    return Container(
      padding: const EdgeInsets.symmetric(vertical: 12),
      decoration: BoxDecoration(border: isLast ? null : Border(bottom: BorderSide(color: AppColors.border))),
      child: Row(
        children: [
          Text(icon, style: const TextStyle(fontSize: 20)),
          const SizedBox(width: 12),
          Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [Text(title, style: const TextStyle(color: Colors.white, fontSize: 13, fontWeight: FontWeight.w600)), const SizedBox(height: 2), Text(desc, style: const TextStyle(color: Color(0xFF9CA3AF), fontSize: 11))])),
          const Icon(Icons.chevron_right, color: Color(0xFF6B7280), size: 20),
        ],
      ),
    );
  }
}
