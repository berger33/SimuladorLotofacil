import 'package:hive_flutter/hive_flutter.dart';

class HiveInit {
  static Future<void> init() async {
    await Hive.initFlutter();
    
    // Abre boxes essenciais
    await Hive.openBox('settings');
    await Hive.openBox('ranking');
    await Hive.openBox('sorteios');
    await Hive.openBox('matrizes');
    await Hive.openBox('cache');
    await Hive.openBox('analytics');
  }
  
  static Box get settings => Hive.box('settings');
  static Box get ranking => Hive.box('ranking');
  static Box get sorteios => Hive.box('sorteios');
  static Box get matrizes => Hive.box('matrizes');
  
  static bool isOnboardingCompleted() {
    return settings.get('onboarding_completed', defaultValue: false);
  }
  
  static Future<void> setOnboardingCompleted(bool value) async {
    await settings.put('onboarding_completed', value);
  }
  
  static bool isPremium() {
    return settings.get('is_premium', defaultValue: false);
  }
  
  static Future<void> setPremium(bool value) async {
    await settings.put('is_premium', value);
  }
  
  static int getGeracoesCount() {
    return settings.get('geracoes_count', defaultValue: 0);
  }
  
  static Future<void> incrementGeracoes() async {
    var count = getGeracoesCount();
    await settings.put('geracoes_count', count + 1);
  }
}
