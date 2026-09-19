import 'package:equatable/equatable.dart';

class EstatisticasAcertos extends Equatable {
  final int h11, h12, h13, h14, h15, ruins;
  
  const EstatisticasAcertos({
    this.h11 = 0, this.h12 = 0, this.h13 = 0, this.h14 = 0, this.h15 = 0, this.ruins = 0,
  });
  
  int get total => h11 + h12 + h13 + h14 + h15 + ruins;
  
  @override
  List<Object?> get props => [h11, h12, h13, h14, h15, ruins];
  
  factory EstatisticasAcertos.fromJson(Map<String, dynamic> json) {
    return EstatisticasAcertos(
      h11: json['h11'] ?? 0,
      h12: json['h12'] ?? 0,
      h13: json['h13'] ?? 0,
      h14: json['h14'] ?? 0,
      h15: json['h15'] ?? 0,
      ruins: json['ruins'] ?? 0,
    );
  }
  
  Map<String, dynamic> toJson() => {
    'h11': h11, 'h12': h12, 'h13': h13, 'h14': h14, 'h15': h15, 'ruins': ruins,
  };
}

class Matriz extends Equatable {
  final String id;
  final List<int> base20;
  final List<List<int>> sistema;
  final double score;
  final EstatisticasAcertos stats;
  final int geracao;
  final DateTime timestamp;
  final int qtdJogos;
  final bool favorita;
  final bool relaxou;
  final double sharpe;
  
  const Matriz({
    required this.id,
    required this.base20,
    required this.sistema,
    required this.score,
    required this.stats,
    required this.geracao,
    required this.timestamp,
    required this.qtdJogos,
    this.favorita = false,
    this.relaxou = false,
    this.sharpe = 0.0,
  });
  
  @override
  List<Object?> get props => [id, base20, score, geracao, timestamp];
  
  double get lucroMedio => sistema.isEmpty ? 0 : score / sistema.length;
  
  Matriz copyWith({
    bool? favorita,
  }) {
    return Matriz(
      id: id,
      base20: base20,
      sistema: sistema,
      score: score,
      stats: stats,
      geracao: geracao,
      timestamp: timestamp,
      qtdJogos: qtdJogos,
      favorita: favorita ?? this.favorita,
      relaxou: relaxou,
      sharpe: sharpe,
    );
  }
}

class Sorteio extends Equatable {
  final int concurso;
  final String data;
  final Set<int> dezenas;
  
  const Sorteio({required this.concurso, required this.data, required this.dezenas});
  
  @override
  List<Object?> get props => [concurso, data, dezenas];
}

class AnaliseAtraso extends Equatable {
  final int dezena;
  final int atual;
  final double media;
  final double limite;
  final String status;
  
  const AnaliseAtraso({
    required this.dezena,
    required this.atual,
    required this.media,
    required this.limite,
    required this.status,
  });
  
  bool get isEstourando => status == "ESTOURANDO";
  
  @override
  List<Object?> get props => [dezena, atual, media, limite, status];
}
