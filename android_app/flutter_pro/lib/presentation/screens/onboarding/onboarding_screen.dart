import 'package:flutter/material.dart';
import 'package:hive_flutter/hive_flutter.dart';
import '../../../core/constants/colors.dart';
import '../../../core/constants/strings.dart';

class OnboardingScreen extends StatefulWidget {
  final VoidCallback onCompleted;
  const OnboardingScreen({super.key, required this.onCompleted});

  @override
  State<OnboardingScreen> createState() => _OnboardingScreenState();
}

class _OnboardingScreenState extends State<OnboardingScreen> {
  final PageController _controller = PageController();
  int _currentPage = 0;

  final List<Map<String, String>> _pages = [
    {
      'title': AppStrings.onboardingTitle1,
      'desc': AppStrings.onboardingDesc1,
      'emoji': '🚀',
    },
    {
      'title': AppStrings.onboardingTitle2,
      'desc': '🧬 Algoritmo Genético evolui matrizes\n🤖 IA prevê padrões\n🎯 Fechamento inteligente',
      'emoji': '🧠',
    },
    {
      'title': AppStrings.onboardingTitle3,
      'desc': AppStrings.onboardingDesc3,
      'emoji': '⚠️',
    },
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        children: [
          Expanded(
            child: PageView.builder(
              controller: _controller,
              onPageChanged: (i) => setState(() => _currentPage = i),
              itemCount: _pages.length,
              itemBuilder: (context, i) {
                var page = _pages[i];
                return Padding(
                  padding: const EdgeInsets.all(32),
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Text(page['emoji']!, style: const TextStyle(fontSize: 80)),
                      const SizedBox(height: 32),
                      Text(
                        page['title']!,
                        style: Theme.of(context).textTheme.headlineMedium?.copyWith(fontWeight: FontWeight.bold),
                        textAlign: TextAlign.center,
                      ),
                      const SizedBox(height: 16),
                      Text(
                        page['desc']!,
                        style: Theme.of(context).textTheme.bodyLarge,
                        textAlign: TextAlign.center,
                      ),
                    ],
                  ),
                );
              },
            ),
          ),
          // Indicators
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: List.generate(_pages.length, (i) => Container(
              margin: const EdgeInsets.all(4),
              width: _currentPage == i ? 24 : 8,
              height: 8,
              decoration: BoxDecoration(
                color: _currentPage == i ? AppColors.primary : Colors.grey,
                borderRadius: BorderRadius.circular(4),
              ),
            )),
          ),
          const SizedBox(height: 24),
          Padding(
            padding: const EdgeInsets.all(24),
            child: Column(
              children: [
                if (_currentPage < _pages.length - 1)
                  FilledButton(
                    onPressed: () => _controller.nextPage(duration: const Duration(milliseconds: 300), curve: Curves.easeInOut),
                    style: FilledButton.styleFrom(minimumSize: const Size.fromHeight(56)),
                    child: const Text('Próximo'),
                  )
                else
                  Column(
                    children: [
                      Row(
                        children: [
                          Checkbox(value: true, onChanged: (_) {}),
                          const Expanded(child: Text('Li e aceito o aviso legal e jogo responsável +18')),
                        ],
                      ),
                      const SizedBox(height: 12),
                      FilledButton(
                        onPressed: () async {
                          var box = Hive.box('settings');
                          await box.put('onboarding_completed', true);
                          widget.onCompleted();
                        },
                        style: FilledButton.styleFrom(
                          backgroundColor: AppColors.success,
                          minimumSize: const Size.fromHeight(56),
                        ),
                        child: const Text('Começar 🚀'),
                      ),
                    ],
                  ),
                const SizedBox(height: 12),
                TextButton(
                  onPressed: () async {
                    if (_currentPage == _pages.length - 1) {
                      var box = Hive.box('settings');
                      await box.put('onboarding_completed', true);
                      widget.onCompleted();
                    } else {
                      _controller.jumpToPage(_pages.length - 1);
                    }
                  },
                  child: Text(_currentPage == _pages.length - 1 ? 'Aceitar e continuar' : 'Pular'),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
