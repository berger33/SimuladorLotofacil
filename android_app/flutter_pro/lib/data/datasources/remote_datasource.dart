import 'dart:async';
import 'package:dio/dio.dart';
import '../../domain/entities/matriz.dart';
import '../../domain/usecases/gerar_matriz.dart';
import '../models/matriz_model.dart';

class RemoteDataSource {
  final Dio dio;
  final String baseUrl;
  
  RemoteDataSource({required this.dio, this.baseUrl = 'https://api.lotofacilpro.com'});
  
  Stream<Matriz> gerarMatrizStream(GerarMatrizParams params) async* {
    // Tenta chamar API real com SSE ou polling
    // Por enquanto, lança exceção para fallback local
    // Quando backend estiver pronto, implementar:
    // var response = await dio.post('/api/v1/gerar/stream', data: {...});
    throw Exception("Remote não configurado, usando fallback local");
  }
  
  Future<Matriz> gerarMatrizUnica(GerarMatrizParams params) async {
    try {
      var response = await dio.post(
        '$baseUrl/api/v1/gerar',
        data: {
          'num_jogos': params.numJogos,
          'taxa_mutacao': params.taxaMutacao,
          'severidade': params.severidade,
          'filtros': {
            'fixas': params.fixas,
            'bloqueadas': params.bloqueadas,
            'impar': params.impar,
            'moldura': params.moldura,
            'primos': params.primos,
            'soma': params.soma,
          },
          'foco_14': params.foco14,
          'apriori_ativo': params.apriori,
          'auto_piloto': params.autoPiloto,
          'is_premium': params.isPremium,
          'max_geracoes': params.maxGeracoes,
        },
      );
      
      if (response.statusCode == 200) {
        return MatrizModel.fromJson(response.data);
      } else {
        throw Exception("Erro API: ${response.statusCode}");
      }
    } catch (e) {
      throw Exception("Falha ao gerar via API: $e");
    }
  }
  
  Future<List<Map<String, dynamic>>> getAtrasometro() async {
    var response = await dio.get('$baseUrl/api/v1/inteligencia/atrasometro');
    return List<Map<String, dynamic>>.from(response.data['ranking'] ?? []);
  }
  
  Future<List<Map<String, dynamic>>> getMarkov() async {
    var response = await dio.get('$baseUrl/api/v1/inteligencia/markov');
    return List<Map<String, dynamic>>.from(response.data['ranking'] ?? []);
  }
  
  Future<List<Map<String, dynamic>>> getEnsemble({required bool isPremium}) async {
    var response = await dio.get(
      '$baseUrl/api/v1/inteligencia/ensemble',
      queryParameters: {'is_premium': isPremium},
    );
    return List<Map<String, dynamic>>.from(response.data['ranking'] ?? []);
  }
  
  Future<List<int>> getUltimoSorteio() async {
    var response = await dio.get('$baseUrl/api/v1/sorteios/ultimo');
    return List<int>.from(response.data['dezenas'] ?? []);
  }
}
