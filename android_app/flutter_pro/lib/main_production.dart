import 'package:flutter/material.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'package:google_mobile_ads/google_mobile_ads.dart';
import 'app_production.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Hive
  await Hive.initFlutter();
  await Hive.openBox('settings');
  await Hive.openBox('ranking');
  await Hive.openBox('sorteios');
  await Hive.openBox('matrizes');
  await Hive.openBox('cache');
  
  // AdMob (com try/catch para não travar se falhar)
  try {
    await MobileAds.instance.initialize();
  } catch (e) {
    debugPrint('AdMob init falhou (ok para debug): $e');
  }
  
  // Firebase opcional
  // try {
  //   await Firebase.initializeApp(options: DefaultFirebaseOptions.currentPlatform);
  // } catch (e) {
  //   debugPrint('Firebase não configurado: $e');
  // }
  
  runApp(const LotofacilProAppProduction());
}
