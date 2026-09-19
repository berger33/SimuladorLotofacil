import '../../domain/entities/matriz.dart';

class MatrizModel extends Matriz {
  const MatrizModel({
    required super.id,
    required super.base20,
    required super.sistema,
    required super.score,
    required super.stats,
    required super.geracao,
    required super.timestamp,
    required super.qtdJogos,
    super.favorita,
    super.relaxou,
    super.sharpe,
  });
  
  factory MatrizModel.fromJson(Map<String, dynamic> json) {
    return MatrizModel(
      id: json['id'] ?? DateTime.now().millisecondsSinceEpoch.toString(),
      base20: List<int>.from(json['base_20'] ?? json['base20'] ?? []),
      sistema: (json['sistema'] as List? ?? []).map((e) => List<int>.from(e)).toList(),
      score: (json['score'] ?? 0).toDouble(),
      stats: json['stats'] != null 
          ? EstatisticasAcertos.fromJson(json['stats'])
          : EstatisticasAcertos(
              h11: json['h11'] ?? 0,
              h12: json['h12'] ?? 0,
              h13: json['h13'] ?? 0,
              h14: json['h14'] ?? 0,
              h15: json['h15'] ?? 0,
              ruins: json['ruins'] ?? 0,
            ),
      geracao: json['geracao'] ?? 0,
      timestamp: json['timestamp'] != null 
          ? DateTime.parse(json['timestamp'])
          : DateTime.now(),
      qtdJogos: json['qtd_jogos'] ?? json['qtdJogos'] ?? 10,
      favorita: json['favorita'] ?? false,
      relaxou: json['relaxou'] ?? false,
      sharpe: (json['sharpe'] ?? 0).toDouble(),
    );
  }
  
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'base_20': base20,
      'sistema': sistema,
      'score': score,
      'stats': stats.toJson(),
      'geracao': geracao,
      'timestamp': timestamp.toIso8601String(),
      'qtd_jogos': qtdJogos,
      'favorita': favorita,
      'relaxou': relaxou,
      'sharpe': sharpe,
    };
  }
  
  factory MatrizModel.fromEntity(Matriz entity) {
    return MatrizModel(
      id: entity.id,
      base20: entity.base20,
      sistema: entity.sistema,
      score: entity.score,
      stats: entity.stats,
      geracao: entity.geracao,
      timestamp: entity.timestamp,
      qtdJogos: entity.qtdJogos,
      favorita: entity.favorita,
      relaxou: entity.relaxou,
      sharpe: entity.sharpe,
    );
  }
}
