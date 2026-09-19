import 'package:hive_flutter/hive_flutter.dart';
import '../models/matriz_model.dart';
import '../../domain/entities/matriz.dart';

class LocalDataSource {
  static const String rankingBoxName = 'ranking';
  static const String settingsBoxName = 'settings';
  
  Future<Box> _getRankingBox() async {
    if (!Hive.isBoxOpen(rankingBoxName)) {
      return await Hive.openBox(rankingBoxName);
    }
    return Hive.box(rankingBoxName);
  }
  
  Future<void> salvarMatriz(MatrizModel matriz) async {
    var box = await _getRankingBox();
    await box.put(matriz.id, matriz.toJson());
    
    // Mantém só top 50
    var all = box.values.map((e) => MatrizModel.fromJson(Map<String, dynamic>.from(e))).toList();
    all.sort((a,b) => b.score.compareTo(a.score));
    if (all.length > 50) {
      for (var m in all.sublist(50)) {
        await box.delete(m.id);
      }
    }
  }
  
  Future<List<Matriz>> getRanking({int limit = 50}) async {
    var box = await _getRankingBox();
    var all = box.values.map((e) => MatrizModel.fromJson(Map<String, dynamic>.from(e))).toList();
    all.sort((a,b) => b.score.compareTo(a.score));
    return all.take(limit).toList();
  }
  
  Future<void> deletarMatriz(String id) async {
    var box = await _getRankingBox();
    await box.delete(id);
  }
  
  Future<void> favoritarMatriz(String id, bool favorita) async {
    var box = await _getRankingBox();
    var data = box.get(id);
    if (data != null) {
      var matriz = MatrizModel.fromJson(Map<String, dynamic>.from(data));
      var updated = MatrizModel(
        id: matriz.id,
        base20: matriz.base20,
        sistema: matriz.sistema,
        score: matriz.score,
        stats: matriz.stats,
        geracao: matriz.geracao,
        timestamp: matriz.timestamp,
        qtdJogos: matriz.qtdJogos,
        favorita: favorita,
        relaxou: matriz.relaxou,
        sharpe: matriz.sharpe,
      );
      await box.put(id, updated.toJson());
    }
  }
  
  Future<List<Matriz>> getFavoritas() async {
    var ranking = await getRanking(limit: 100);
    return ranking.where((m) => m.favorita).toList();
  }
  
  // Settings
  Future<bool> isOnboardingCompleted() async {
    var box = Hive.box(settingsBoxName);
    return box.get('onboarding_completed', defaultValue: false);
  }
  
  Future<void> setOnboardingCompleted(bool completed) async {
    var box = Hive.box(settingsBoxName);
    await box.put('onboarding_completed', completed);
  }
  
  Future<bool> isPremium() async {
    var box = Hive.box(settingsBoxName);
    return box.get('is_premium', defaultValue: false);
  }
  
  Future<void> setPremium(bool premium) async {
    var box = Hive.box(settingsBoxName);
    await box.put('is_premium', premium);
  }
}
