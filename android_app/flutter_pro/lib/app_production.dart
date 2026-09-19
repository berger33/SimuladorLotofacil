import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'core/constants/colors.dart';
import 'core/theme/app_theme.dart';
import 'core/network/dio_client.dart';
import 'data/datasources/local_datasource.dart';
import 'data/datasources/remote_datasource.dart';
import 'data/repositories/matriz_repository_impl.dart';
import 'domain/usecases/gerar_matriz.dart';
import 'presentation/screens/onboarding/onboarding_screen.dart';
import 'presentation/screens/dashboard/dashboard_screen.dart';
import 'presentation/screens/gerador/gerador_screen.dart';
import 'presentation/screens/inteligencia/inteligencia_screen.dart';
import 'presentation/screens/ranking/ranking_screen.dart';
import 'presentation/screens/premium/premium_screen.dart';
import 'presentation/screens/configuracoes/config_screen.dart';
import 'services/ads_service.dart';
import 'services/iap_service.dart';

class LotofacilProAppProduction extends StatelessWidget {
  const LotofacilProAppProduction({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiRepositoryProvider(
      providers: [
        RepositoryProvider(create: (_) => LocalDataSource()),
        RepositoryProvider(create: (_) => RemoteDataSource(dio: DioClient.create())),
        RepositoryProvider(create: (_) => AdsService()),
        RepositoryProvider(create: (_) => IAPService()),
      ],
      child: MaterialApp(
        title: 'Lotofácil Pro',
        debugShowCheckedModeBanner: false,
        theme: AppTheme.lightTheme,
        darkTheme: AppTheme.darkTheme,
        themeMode: ThemeMode.dark,
        home: const AppInitializer(),
      ),
    );
  }
}

class AppInitializer extends StatefulWidget {
  const AppInitializer({super.key});

  @override
  State<AppInitializer> createState() => _AppInitializerState();
}

class _AppInitializerState extends State<AppInitializer> {
  bool? onboardingCompleted;

  @override
  void initState() {
    super.initState();
    _checkOnboarding();
  }

  Future<void> _checkOnboarding() async {
    await Future.delayed(const Duration(milliseconds: 500));
    var box = Hive.box('settings');
    bool completed = box.get('onboarding_completed', defaultValue: false);
    setState(() {
      onboardingCompleted = completed;
    });
  }

  @override
  Widget build(BuildContext context) {
    if (onboardingCompleted == null) {
      return Scaffold(
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Container(
                width: 80,
                height: 80,
                decoration: const BoxDecoration(
                  gradient: AppColors.gradientPrimary,
                  shape: BoxShape.circle,
                ),
                child: const Icon(Icons.auto_awesome, color: Colors.white, size: 40),
              ),
              const SizedBox(height: 16),
              const CircularProgressIndicator(),
              const SizedBox(height: 16),
              const Text('Lotofácil Pro', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            ],
          ),
        ),
      );
    }

    if (!onboardingCompleted!) {
      return OnboardingScreen(
        onCompleted: () {
          setState(() {
            onboardingCompleted = true;
          });
        },
      );
    }

    return const MainNavigationProduction();
  }
}

class MainNavigationProduction extends StatefulWidget {
  const MainNavigationProduction({super.key});

  @override
  State<MainNavigationProduction> createState() => _MainNavigationProductionState();
}

class _MainNavigationProductionState extends State<MainNavigationProduction> {
  int _currentIndex = 0;

  final _screens = [
    const DashboardScreen(),
    const GeradorScreen(),
    const InteligenciaScreen(),
    const RankingScreen(),
    const PremiumScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _screens[_currentIndex],
      bottomNavigationBar: NavigationBar(
        selectedIndex: _currentIndex,
        onDestinationSelected: (i) => setState(() => _currentIndex = i),
        destinations: const [
          NavigationDestination(icon: Icon(Icons.dashboard_outlined), selectedIcon: Icon(Icons.dashboard), label: 'Dashboard'),
          NavigationDestination(icon: Icon(Icons.auto_fix_high_outlined), selectedIcon: Icon(Icons.auto_fix_high), label: 'Gerador'),
          NavigationDestination(icon: Icon(Icons.psychology_outlined), selectedIcon: Icon(Icons.psychology), label: 'IA'),
          NavigationDestination(icon: Icon(Icons.emoji_events_outlined), selectedIcon: Icon(Icons.emoji_events), label: 'Ranking'),
          NavigationDestination(icon: Icon(Icons.workspace_premium_outlined), selectedIcon: Icon(Icons.workspace_premium), label: 'Pro'),
        ],
      ),
    );
  }
}
