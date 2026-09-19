import '../entities/matriz.dart';
import '../usecases/gerar_matriz.dart';

abstract class MatrizRepository {
  Stream<Matriz> gerarMatrizStream(GerarMatrizParams params);
  Future<Matriz> gerarMatrizUnica(GerarMatrizParams params);
  Future<List<Matriz>> getRanking({int limit = 50});
  Future<void> salvarMatriz(Matriz matriz);
  Future<void> deletarMatriz(String id);
  Future<void> favoritarMatriz(String id, bool favorita);
  Future<List<Matriz>> getFavoritas();
}

abstract class SorteioRepository {
  Future<List<Sorteio>> getSorteios({int limit = 100});
  Future<Sorteio?> getUltimoSorteio();
  Future<Map<int, int>> getFrequencia();
}

abstract class InteligenciaRepository {
  Future<List<AnaliseAtraso>> getAtrasometro();
  Future<List<Map<String, dynamic>>> getMarkov();
  Future<List<Map<String, dynamic>>> getEnsemble({required bool isPremium});
  Future<List<Set<int>>> getApriori({required bool isPremium});
  Future<Map<String, int>> getAutopiloto({required bool isPremium});
}
