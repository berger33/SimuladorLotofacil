import 'package:flutter/material.dart';
import '../../core/constants/colors.dart';

class HeatmapWidget extends StatelessWidget {
  final Map<int, double> frequencia; // dezena -> score normalizado 0-1
  final Function(int)? onTapDezena;
  
  const HeatmapWidget({
    super.key,
    required this.frequencia,
    this.onTapDezena,
  });

  @override
  Widget build(BuildContext context) {
    return GridView.builder(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 5,
        mainAxisSpacing: 8,
        crossAxisSpacing: 8,
        childAspectRatio: 1.2,
      ),
      itemCount: 25,
      itemBuilder: (context, i) {
        int dezena = i + 1;
        double score = frequencia[dezena] ?? 0.0;
        Color color = _getColorForScore(score);
        
        return GestureDetector(
          onTap: () => onTapDezena?.call(dezena),
          child: AnimatedContainer(
            duration: const Duration(milliseconds: 300),
            decoration: BoxDecoration(
              color: color,
              borderRadius: BorderRadius.circular(12),
              boxShadow: [
                BoxShadow(
                  color: color.withOpacity(0.3),
                  blurRadius: 4,
                  offset: const Offset(0, 2),
                ),
              ],
            ),
            child: Center(
              child: Text(
                dezena.toString().padLeft(2, '0'),
                style: const TextStyle(
                  fontWeight: FontWeight.bold,
                  color: Colors.white,
                  fontSize: 16,
                ),
              ),
            ),
          ),
        );
      },
    );
  }
  
  Color _getColorForScore(double score) {
    // score 0-1 -> cold to hot
    if (score < 0.2) return AppColors.heatCold.withOpacity(0.6);
    if (score < 0.4) return AppColors.heatCold;
    if (score < 0.6) return AppColors.heatWarm;
    if (score < 0.8) return AppColors.heatHot;
    return AppColors.heatBurn;
  }
}

class HeatmapLegend extends StatelessWidget {
  const HeatmapLegend({super.key});

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
      children: [
        _legendItem(AppColors.heatCold.withOpacity(0.6), "Fria"),
        _legendItem(AppColors.heatCold, "Média"),
        _legendItem(AppColors.heatWarm, "Quente"),
        _legendItem(AppColors.heatBurn, "Muito Quente"),
      ],
    );
  }
  
  Widget _legendItem(Color color, String label) {
    return Row(
      children: [
        Container(width: 12, height: 12, decoration: BoxDecoration(color: color, borderRadius: BorderRadius.circular(2))),
        const SizedBox(width: 4),
        Text(label, style: const TextStyle(fontSize: 12)),
      ],
    );
  }
}
