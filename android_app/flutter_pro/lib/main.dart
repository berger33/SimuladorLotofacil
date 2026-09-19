import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:google_mobile_ads/google_mobile_ads.dart';
import 'app.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Hive - local storage
  await Hive.initFlutter();
  await Hive.openBox('settings');
  await Hive.openBox('ranking');
  await Hive.openBox('sorteios');
  await Hive.openBox('matrizes');
  
  // Firebase (opcional, se configurado)
  try {
    await Firebase.initializeApp();
  } catch (e) {
    debugPrint('Firebase não configurado, continuando sem: $e');
  }
  
  // AdMob
  try {
    await MobileAds.instance.initialize();
  } catch (e) {
    debugPrint('AdMob init falhou: $e');
  }
  
  runApp(const LotofacilProApp());
}
