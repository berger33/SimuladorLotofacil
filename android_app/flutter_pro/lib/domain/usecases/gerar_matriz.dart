import '../entities/matriz.dart';
import '../repositories/matriz_repository.dart';

class GerarMatrizParams {
  final int numJogos;
  final List<int> fixas;
  final List<int> bloqueadas;
  final int? impar;
  final int? moldura;
  final int? primos;
  final int? soma;
  final bool foco14;
  final double taxaMutacao;
  final double severidade;
  final bool apriori;
  final bool autoPiloto;
  final bool isPremium;
  final int maxGeracoes;
  
  const GerarMatrizParams({
    this.numJogos = 10,
    this.fixas = const [],
    this.bloqueadas = const [],
    this.impar,
    this.moldura,
    this.primos,
    this.soma,
    this.foco14 = false,
    this.taxaMutacao = 0.05,
    this.severidade = 0.8,
    this.apriori = false,
    this.autoPiloto = false,
    this.isPremium = false,
    this.maxGeracoes = 50,
  });
}

class GerarMatrizUseCase {
  final MatrizRepository repository;
  
  GerarMatrizUseCase(this.repository);
  
  Stream<Matriz> call(GerarMatrizParams params) {
    // Validação freemium
    if (!params.isPremium && params.numJogos > 10) {
      throw Exception("Free limita 10 jogos. Assine Pro para 33.");
    }
    if (!params.isPremium && (params.apriori || params.autoPiloto)) {
      throw Exception("Apriori e Auto-Piloto são Pro");
    }
    
    return repository.gerarMatrizStream(params);
  }
  
  Future<Matriz> gerarUnica(GerarMatrizParams params) {
    return repository.gerarMatrizUnica(params);
  }
}

class GetRankingUseCase {
  final MatrizRepository repository;
  GetRankingUseCase(this.repository);
  
  Future<List<Matriz>> call({int limit = 50}) {
    return repository.getRanking(limit: limit);
  }
}

class SalvarMatrizUseCase {
  final MatrizRepository repository;
  SalvarMatrizUseCase(this.repository);
  
  Future<void> call(Matriz matriz) {
    return repository.salvarMatriz(matriz);
  }
}
