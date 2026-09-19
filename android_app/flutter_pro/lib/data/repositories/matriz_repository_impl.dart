import 'dart:async';
import 'dart:math';
import '../../domain/entities/matriz.dart';
import '../../domain/repositories/matriz_repository.dart';
import '../../domain/usecases/gerar_matriz.dart';
import '../models/matriz_model.dart';
import '../datasources/local_datasource.dart';
import '../datasources/remote_datasource.dart';

class MatrizRepositoryImpl implements MatrizRepository {
  final LocalDataSource local;
  final RemoteDataSource remote;
  
  MatrizRepositoryImpl({required this.local, required this.remote});
  
  @override
  Stream<Matriz> gerarMatrizStream(GerarMatrizParams params) async* {
    // Tenta remote primeiro, fallback para local mock
    try {
      // Se tem remote configurado, usa
      yield* remote.gerarMatrizStream(params);
    } catch (e) {
      // Fallback: geração local mock (para MVP sem backend)
      yield* _gerarLocalMock(params);
    }
  }
  
  Stream<Matriz> _gerarLocalMock(GerarMatrizParams params) async* {
    final random = Random();
    List<int> base20 = List.generate(20, (i) => i+1);
    // Aplica fixas
    if (params.fixas.isNotEmpty) {
      for (var f in params.fixas.take(5)) {
        if (!base20.contains(f)) {
          base20[0] = f;
        }
      }
      base20 = base20.toSet().toList()..sort();
      while (base20.length < 20) {
        base20.add(random.nextInt(25)+1);
        base20 = base20.toSet().toList();
      }
      base20 = base20.take(20).toList()..sort();
    } else {
      base20 = (List.generate(25, (i) => i+1)..shuffle()).take(20).toList()..sort();
    }
    
    double melhorScore = -1000;
    
    for (int g = 0; g < params.maxGeracoes; g++) {
      await Future.delayed(Duration(milliseconds: 300));
      
      // Simula evolução
      if (g > 0) {
        // Mutação leve na base
        if (random.nextDouble() < params.taxaMutacao) {
          base20[random.nextInt(20)] = random.nextInt(25)+1;
          base20 = base20.toSet().toList();
          while (base20.length < 20) {
            base20.add(random.nextInt(25)+1);
            base20 = base20.toSet().toList();
          }
          base20 = base20.take(20).toList()..sort();
        }
      }
      
      double score = random.nextDouble() * 500 - 50 + (g * 2); // melhora com gerações
      if (score > melhorScore) melhorScore = score;
      
      List<List<int>> sistema = List.generate(params.numJogos, (_) {
        var jogo = (base20.toList()..shuffle()).take(15).toList()..sort();
        return jogo;
      });
      
      var matriz = Matriz(
        id: DateTime.now().millisecondsSinceEpoch.toString(),
        base20: base20,
        sistema: sistema,
        score: melhorScore,
        stats: EstatisticasAcertos(
          h11: random.nextInt(20),
          h12: random.nextInt(10),
          h13: random.nextInt(5),
          h14: random.nextInt(2),
          h15: random.nextInt(1),
          ruins: random.nextInt(200),
        ),
        geracao: g,
        timestamp: DateTime.now(),
        qtdJogos: params.numJogos,
      );
      
      // Salva automaticamente top 3
      if (g % 10 == 0 || g == params.maxGeracoes -1) {
        await local.salvarMatriz(MatrizModel.fromEntity(matriz));
      }
      
      yield matriz;
    }
  }
  
  @override
  Future<Matriz> gerarMatrizUnica(GerarMatrizParams params) async {
    try {
      return await remote.gerarMatrizUnica(params);
    } catch (e) {
      // Fallback local
      var stream = _gerarLocalMock(params.copyWithMaxGeracoes(1));
      return await stream.first;
    }
  }
  
  @override
  Future<List<Matriz>> getRanking({int limit = 50}) async {
    try {
      var localRanking = await local.getRanking(limit: limit);
      if (localRanking.isNotEmpty) return localRanking;
    } catch (_) {}
    
    // Mock ranking se vazio
    return List.generate(10, (i) {
      return Matriz(
        id: 'mock_$i',
        base20: (List.generate(25, (j) => j+1)..shuffle()).take(20).toList()..sort(),
        sistema: List.generate(10, (_) => (List.generate(25, (j) => j+1)..shuffle()).take(15).toList()..sort()),
        score: 1000 - i*50 + Random().nextDouble()*100,
        stats: EstatisticasAcertos(h11: 10+i, h12: 5, h13: 2, h14: 1, h15: 0, ruins: 100),
        geracao: 42+i,
        timestamp: DateTime.now().subtract(Duration(days: i)),
        qtdJogos: 10,
      );
    });
  }
  
  @override
  Future<void> salvarMatriz(Matriz matriz) => local.salvarMatriz(MatrizModel.fromEntity(matriz));
  
  @override
  Future<void> deletarMatriz(String id) => local.deletarMatriz(id);
  
  @override
  Future<void> favoritarMatriz(String id, bool favorita) => local.favoritarMatriz(id, favorita);
  
  @override
  Future<List<Matriz>> getFavoritas() => local.getFavoritas();
}

extension on GerarMatrizParams {
  GerarMatrizParams copyWithMaxGeracoes(int max) {
    return GerarMatrizParams(
      numJogos: numJogos,
      fixas: fixas,
      bloqueadas: bloqueadas,
      impar: impar,
      moldura: moldura,
      primos: primos,
      soma: soma,
      foco14: foco14,
      taxaMutacao: taxaMutacao,
      severidade: severidade,
      apriori: apriori,
      autoPiloto: autoPiloto,
      isPremium: isPremium,
      maxGeracoes: max,
    );
  }
}
