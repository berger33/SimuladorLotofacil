import 'package:flutter/material.dart';
import '../../domain/entities/matriz.dart';
import '../../core/constants/colors.dart';

class CardMatriz extends StatelessWidget {
  final Matriz matriz;
  final int posicao;
  final VoidCallback? onTap;
  final VoidCallback? onDelete;
  final VoidCallback? onFavorite;
  
  const CardMatriz({
    super.key,
    required this.matriz,
    required this.posicao,
    this.onTap,
    this.onDelete,
    this.onFavorite,
  });

  @override
  Widget build(BuildContext context) {
    bool isTop3 = posicao <= 3;
    bool isPositive = matriz.score > 0;
    
    return Card(
      elevation: isTop3 ? 4 : 2,
      color: isTop3 ? AppColors.surfaceDark : null,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
        side: isTop3 ? BorderSide(color: _getRankColor(posicao), width: 2) : BorderSide.none,
      ),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(16),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  CircleAvatar(
                    backgroundColor: _getRankColor(posicao),
                    radius: 20,
                    child: Text(
                      '$posicao',
                      style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'R\$ ${matriz.score.toStringAsFixed(2)}',
                          style: TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                            color: isPositive ? AppColors.success : AppColors.error,
                          ),
                        ),
                        Text(
                          'G${matriz.geracao} • ${matriz.qtdJogos} jogos • R\$ ${matriz.lucroMedio.toStringAsFixed(2)}/ap',
                          style: Theme.of(context).textTheme.bodySmall,
                        ),
                      ],
                    ),
                  ),
                  if (matriz.favorita) const Icon(Icons.star, color: AppColors.tertiary),
                  PopupMenuButton(
                    itemBuilder: (c) => [
                      const PopupMenuItem(value: 'fav', child: Text('Favoritar')),
                      const PopupMenuItem(value: 'share', child: Text('Compartilhar')),
                      const PopupMenuItem(value: 'delete', child: Text('Deletar')),
                    ],
                    onSelected: (v) {
                      if (v == 'fav' && onFavorite != null) onFavorite!();
                      if (v == 'delete' && onDelete != null) onDelete!();
                    },
                  ),
                ],
              ),
              const SizedBox(height: 12),
              // Base 20
              Container(
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(
                  color: AppColors.primary.withOpacity(0.1),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Row(
                  children: [
                    const Icon(Icons.stars, size: 16, color: AppColors.primary),
                    const SizedBox(width: 8),
                    Expanded(
                      child: Text(
                        matriz.base20.map((n) => n.toString().padLeft(2, '0')).join(' '),
                        style: const TextStyle(fontFamily: 'monospace', fontSize: 13, fontWeight: FontWeight.w500),
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 8),
              // Stats
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  _statChip('11', matriz.stats.h11, Colors.grey),
                  _statChip('12', matriz.stats.h12, Colors.blueGrey),
                  _statChip('13', matriz.stats.h13, Colors.blue),
                  _statChip('14', matriz.stats.h14, AppColors.warning),
                  _statChip('15', matriz.stats.h15, AppColors.success),
                ],
              ),
              if (matriz.relaxou)
                Padding(
                  padding: const EdgeInsets.only(top: 8),
                  child: Row(
                    children: [
                      const Icon(Icons.warning_amber, size: 14, color: AppColors.warning),
                      const SizedBox(width: 4),
                      Text('Filtros relaxados', style: TextStyle(fontSize: 11, color: AppColors.warning)),
                    ],
                  ),
                ),
            ],
          ),
        ),
      ),
    );
  }
  
  Widget _statChip(String label, int value, Color color) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      decoration: BoxDecoration(
        color: color.withOpacity(0.15),
        borderRadius: BorderRadius.circular(6),
        border: Border.all(color: color.withOpacity(0.3)),
      ),
      child: Column(
        children: [
          Text(label, style: TextStyle(fontSize: 10, color: color, fontWeight: FontWeight.bold)),
          Text('$value', style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: color)),
        ],
      ),
    );
  }
  
  Color _getRankColor(int pos) {
    if (pos == 1) return AppColors.tertiary;
    if (pos == 2) return Colors.grey;
    if (pos == 3) return const Color(0xFFCD7F32); // bronze
    return AppColors.primary;
  }
}
