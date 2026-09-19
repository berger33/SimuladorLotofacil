import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../../../core/constants/colors.dart';
import '../../../domain/usecases/gerar_matriz.dart';
import '../../../data/datasources/local_datasource.dart';
import '../../../data/datasources/remote_datasource.dart';
import '../../../data/repositories/matriz_repository_impl.dart';
import '../../../core/network/dio_client.dart';
import '../../blocs/gerador/gerador_bloc.dart';
import '../../../services/ads_service.dart';
import '../../../services/iap_service.dart';
import '../../widgets/card_matriz.dart';

class GeradorScreen extends StatefulWidget {
  const GeradorScreen({super.key});

  @override
  State<GeradorScreen> createState() => _GeradorScreenState();
}

class _GeradorScreenState extends State<GeradorScreen> {
  int qtdJogos = 10;
  List<int> fixas = [];
  List<int> bloqueadas = [];
  int? filtroImpar;
  int? filtroMoldura;
  int? filtroPrimos;
  bool foco14 = false;
  double mutacao = 5;
  double severidade = 80;
  bool apriori = false;
  bool autoPiloto = false;
  bool memoria = true;
  bool hamming = false;

  final fixasController = TextEditingController();
  final bloqueadasController = TextEditingController();

  @override
  void dispose() {
    fixasController.dispose();
    bloqueadasController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (context) => GeradorBloc(
        gerarMatrizUseCase: GerarMatrizUseCase(
          MatrizRepositoryImpl(
            local: LocalDataSource(),
            remote: RemoteDataSource(dio: DioClient.create()),
          ),
        ),
        adsService: AdsService(),
        iapService: IAPService(),
      ),
      child: Scaffold(
        appBar: AppBar(
          title: const Text('Gerador'),
          actions: [
            IconButton(icon: const Icon(Icons.info_outline), onPressed: () => _showInfo()),
          ],
        ),
        body: BlocConsumer<GeradorBloc, GeradorState>(
          listener: (context, state) {
            if (state is GeradorPremiumRequired) {
              _showPremiumPaywall(state.feature);
            }
            if (state is GeradorError) {
              ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(state.message), backgroundColor: AppColors.error));
            }
            if (state is GeradorSuccess) {
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(content: Text('✅ Matriz gerada! Score R\$ ${state.matriz.score.toStringAsFixed(2)}'), backgroundColor: AppColors.success),
              );
            }
          },
          builder: (context, state) {
            return Stack(
              children: [
                ListView(
                  padding: const EdgeInsets.all(16),
                  children: [
                    // Qtd Jogos
                    Card(
                      child: Padding(
                        padding: const EdgeInsets.all(16),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text('🎯 Quantidade de Jogos', style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold)),
                            const SizedBox(height: 12),
                            SegmentedButton<int>(
                              segments: const [
                                ButtonSegment(value: 10, label: Text('10 Free')),
                                ButtonSegment(value: 15, label: Text('15')),
                                ButtonSegment(value: 20, label: Text('20 Pro')),
                                ButtonSegment(value: 33, label: Text('33 Pro')),
                              ],
                              selected: {qtdJogos},
                              onSelectionChanged: (s) => setState(() => qtdJogos = s.first),
                            ),
                            const SizedBox(height: 8),
                            if (qtdJogos > 10)
                              Container(
                                padding: const EdgeInsets.all(8),
                                decoration: BoxDecoration(color: AppColors.tertiary.withOpacity(0.15), borderRadius: BorderRadius.circular(8)),
                                child: Row(
                                  children: [
                                    const Icon(Icons.workspace_premium, size: 16, color: AppColors.tertiary),
                                    const SizedBox(width: 8),
                                    Expanded(child: Text('$qtdJogos jogos é Pro. Free limita 10.', style: const TextStyle(fontSize: 12))),
                                  ],
                                ),
                              ),
                          ],
                        ),
                      ),
                    ),
                    const SizedBox(height: 12),

                    // DNA
                    Card(
                      child: Padding(
                        padding: const EdgeInsets.all(16),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text('🧬 Engenharia de DNA', style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold)),
                            const SizedBox(height: 12),
                            TextField(
                              controller: fixasController,
                              decoration: const InputDecoration(
                                labelText: 'Matriz Ímã (Fixas): 01, 05, 10',
                                border: OutlineInputBorder(),
                                prefixIcon: Icon(Icons.push_pin),
                                helperText: 'Dezenas que estarão em todos os jogos',
                              ),
                              onChanged: (v) {
                                setState(() {
                                  fixas = v.split(',').map((e) => int.tryParse(e.trim()) ?? 0).where((e) => e >= 1 && e <= 25).toList();
                                });
                              },
                            ),
                            const SizedBox(height: 8),
                            if (fixas.isNotEmpty)
                              Wrap(
                                spacing: 6,
                                children: fixas.map((n) => Chip(
                                  label: Text(n.toString().padLeft(2, '0')),
                                  backgroundColor: AppColors.tertiary.withOpacity(0.2),
                                  deleteIcon: const Icon(Icons.close, size: 16),
                                  onDeleted: () {
                                    setState(() {
                                      fixas.remove(n);
                                      fixasController.text = fixas.join(', ');
                                    });
                                  },
                                )).toList(),
                              ),
                            const SizedBox(height: 12),
                            TextField(
                              controller: bloqueadasController,
                              decoration: const InputDecoration(
                                labelText: 'Lista Negra (Banidas): 25',
                                border: OutlineInputBorder(),
                                prefixIcon: Icon(Icons.block),
                                helperText: 'Dezenas que nunca entram',
                              ),
                              onChanged: (v) {
                                setState(() {
                                  bloqueadas = v.split(',').map((e) => int.tryParse(e.trim()) ?? 0).where((e) => e >= 1 && e <= 25).toList();
                                });
                              },
                            ),
                            const SizedBox(height: 8),
                            if (bloqueadas.isNotEmpty)
                              Wrap(
                                spacing: 6,
                                children: bloqueadas.map((n) => Chip(
                                  label: Text(n.toString().padLeft(2, '0')),
                                  backgroundColor: AppColors.error.withOpacity(0.2),
                                  deleteIcon: const Icon(Icons.close, size: 16),
                                  onDeleted: () {
                                    setState(() {
                                      bloqueadas.remove(n);
                                      bloqueadasController.text = bloqueadas.join(', ');
                                    });
                                  },
                                )).toList(),
                              ),
                          ],
                        ),
                      ),
                    ),
                    const SizedBox(height: 12),

                    // Filtros
                    Card(
                      child: Padding(
                        padding: const EdgeInsets.all(16),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text('🎛️ Filtros e Fechamento', style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold)),
                            const SizedBox(height: 8),
                            SwitchListTile(
                              title: const Text('🎯 Auto-Piloto XGBoost (Pro)'),
                              subtitle: const Text('Prevê filtros automaticamente'),
                              value: autoPiloto,
                              onChanged: (v) => setState(() => autoPiloto = v),
                            ),
                            const Divider(),
                            Wrap(
                              spacing: 8,
                              children: [
                                FilterChip(
                                  label: const Text('Ímpares 7-8'),
                                  selected: filtroImpar != null,
                                  onSelected: (v) => setState(() => filtroImpar = v ? 8 : null),
                                ),
                                FilterChip(
                                  label: const Text('Moldura 9-11'),
                                  selected: filtroMoldura != null,
                                  onSelected: (v) => setState(() => filtroMoldura = v ? 10 : null),
                                ),
                                FilterChip(
                                  label: const Text('Primos 4-6'),
                                  selected: filtroPrimos != null,
                                  onSelected: (v) => setState(() => filtroPrimos = v ? 5 : null),
                                ),
                                FilterChip(
                                  label: const Text('🎯 Cofre Seguro (Foco 14)'),
                                  selected: foco14,
                                  onSelected: (v) => setState(() => foco14 = v),
                                ),
                              ],
                            ),
                            const SizedBox(height: 8),
                            Container(
                              padding: const EdgeInsets.all(8),
                              decoration: BoxDecoration(color: AppColors.info.withOpacity(0.1), borderRadius: BorderRadius.circular(8)),
                              child: const Text('💡 Se filtros muito restritos, sistema aplica relaxamento automático (+1/-1) para não travar.',
                                  style: TextStyle(fontSize: 11)),
                            ),
                          ],
                        ),
                      ),
                    ),
                    const SizedBox(height: 12),

                    // Hiperparâmetros
                    Card(
                      child: Padding(
                        padding: const EdgeInsets.all(16),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text('🎚️ Hiperparâmetros', style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold)),
                            const SizedBox(height: 12),
                            Row(
                              children: [
                                const Text('Mutação'),
                                const Spacer(),
                                Container(
                                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                                  decoration: BoxDecoration(color: AppColors.primary.withOpacity(0.15), borderRadius: BorderRadius.circular(8)),
                                  child: Text('${mutacao.toInt()}%', style: const TextStyle(fontWeight: FontWeight.bold)),
                                ),
                              ],
                            ),
                            Slider(value: mutacao, min: 1, max: 25, divisions: 24, label: '${mutacao.toInt()}%', onChanged: (v) => setState(() => mutacao = v)),
                            Row(
                              children: [
                                const Text('Severidade Memória'),
                                const Spacer(),
                                Container(
                                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                                  decoration: BoxDecoration(color: AppColors.secondary.withOpacity(0.15), borderRadius: BorderRadius.circular(8)),
                                  child: Text('${severidade.toInt()}%', style: const TextStyle(fontWeight: FontWeight.bold)),
                                ),
                              ],
                            ),
                            Slider(value: severidade, min: 0, max: 100, divisions: 20, label: '${severidade.toInt()}%', onChanged: (v) => setState(() => severidade = v)),
                            SwitchListTile(title: const Text('Memória de Erro'), value: memoria, onChanged: (v) => setState(() => memoria = v)),
                            SwitchListTile(title: const Text('Diversidade Hamming'), value: hamming, onChanged: (v) => setState(() => hamming = v)),
                            SwitchListTile(
                              title: const Text('💎 Mineração Apriori (Pro)'),
                              subtitle: const Text('Bônus para trincas frequentes'),
                              value: apriori,
                              onChanged: (v) => setState(() => apriori = v),
                            ),
                          ],
                        ),
                      ),
                    ),
                    const SizedBox(height: 12),

                    // Estratégias predefinidas
                    Card(
                      child: Padding(
                        padding: const EdgeInsets.all(16),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text('🚀 Estratégias Prontas', style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold)),
                            const SizedBox(height: 8),
                            ListTile(
                              leading: const Icon(Icons.shield, color: AppColors.success),
                              title: const Text('Conservador'),
                              subtitle: const Text('Mutação 2%, Severidade 80%, Foco 14'),
                              onTap: () => setState(() { mutacao = 2; severidade = 80; foco14 = true; }),
                            ),
                            ListTile(
                              leading: const Icon(Icons.local_fire_department, color: AppColors.error),
                              title: const Text('Agressivo (Caos)'),
                              subtitle: const Text('Mutação 15%, Severidade 10%'),
                              onTap: () => setState(() { mutacao = 15; severidade = 10; foco14 = false; }),
                            ),
                            ListTile(
                              leading: const Icon(Icons.smart_toy, color: AppColors.primary),
                              title: const Text('Robô Preguiçoso (IA Total)'),
                              subtitle: const Text('Apriori + Auto-Piloto + RL - Pro'),
                              onTap: () => setState(() { apriori = true; autoPiloto = true; mutacao = 5; }),
                            ),
                          ],
                        ),
                      ),
                    ),
                    const SizedBox(height: 100),
                  ],
                ),
              ),
              // Loading overlay
              if (state is GeradorLoading || state is GeradorProgress)
                Container(
                  color: Colors.black54,
                  child: Center(
                    child: Card(
                      margin: const EdgeInsets.all(24),
                      child: Padding(
                        padding: const EdgeInsets.all(24),
                        child: Column(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            const CircularProgressIndicator(),
                            const SizedBox(height: 16),
                            Text(
                              state is GeradorProgress
                                  ? 'Geração ${state.geracaoAtual}/${state.maxGeracoes}\nScore R\$ ${state.matriz.score.toStringAsFixed(2)}'
                                  : 'Iniciando motor...',
                              textAlign: TextAlign.center,
                              style: Theme.of(context).textTheme.titleMedium,
                            ),
                            const SizedBox(height: 8),
                            if (state is GeradorProgress)
                              Text(
                                'Base: ${state.matriz.base20.map((n) => n.toString().padLeft(2, '0')).join(' ')}',
                                style: const TextStyle(fontFamily: 'monospace', fontSize: 11),
                                textAlign: TextAlign.center,
                              ),
                            const SizedBox(height: 16),
                            Row(
                              children: [
                                Expanded(
                                  child: OutlinedButton(
                                    onPressed: () => context.read<GeradorBloc>().add(PararGeracaoEvent()),
                                    child: const Text('Parar'),
                                  ),
                                ),
                              ],
                            ),
                          ],
                        ),
                      ),
                    ),
                  ),
                ),
            ];
          },
        ),
        bottomNavigationBar: Padding(
          padding: const EdgeInsets.all(16),
          child: FilledButton.icon(
            onPressed: () {
              var params = GerarMatrizParams(
                numJogos: qtdJogos,
                fixas: fixas,
                bloqueadas: bloqueadas,
                impar: filtroImpar,
                moldura: filtroMoldura,
                primos: filtroPrimos,
                foco14: foco14,
                taxaMutacao: mutacao / 100,
                severidade: severidade / 100,
                apriori: apriori,
                autoPiloto: autoPiloto,
                isPremium: false, // TODO: checar IAP
                maxGeracoes: 50,
              );
              context.read<GeradorBloc>().add(GerarMatrizEvent(params));
            },
            icon: const Icon(Icons.rocket_launch),
            label: const Text('▶️ Iniciar Motor Híbrido'),
            style: FilledButton.styleFrom(minimumSize: const Size.fromHeight(56)),
          ),
        ),
      ),
    );
  }

  void _showInfo() {
    showDialog(
      context: context,
      builder: (c) => AlertDialog(
        title: const Text('Como funciona?'),
        content: const Text(
          'O motor genético cria 20-30 matrizes mãe, testa contra 3675 sorteios reais, corta as que dão prejuízo e cruza as lucrativas com mutação. A cada geração o lucro médio sobe!\n\n'
          'Dica: Use Robô Preguiçoso para deixar IA configurar tudo.',
        ),
        actions: [TextButton(onPressed: () => Navigator.pop(c), child: const Text('Entendi'))],
      ),
    );
  }

  void _showPremiumPaywall(String feature) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(24))),
      builder: (c) => DraggableScrollableSheet(
        initialChildSize: 0.7,
        maxChildSize: 0.9,
        minChildSize: 0.5,
        expand: false,
        builder: (context, scrollController) => ListView(
          controller: scrollController,
          padding: const EdgeInsets.all(24),
          children: [
            Center(child: Container(width: 40, height: 4, decoration: BoxDecoration(color: Colors.grey[600], borderRadius: BorderRadius.circular(2)))),
            const SizedBox(height: 24),
            const Icon(Icons.workspace_premium, size: 64, color: AppColors.tertiary),
            const SizedBox(height: 16),
            Text('Recurso Premium', style: Theme.of(context).textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.bold), textAlign: TextAlign.center),
            const SizedBox(height: 8),
            Text(feature, textAlign: TextAlign.center),
            const SizedBox(height: 24),
            const Text('✅ 33 jogos (vs 10 free)\n✅ IA completa\n✅ Ilimitado\n✅ Sem anúncios\n✅ Export + Suporte'),
            const SizedBox(height: 24),
            FilledButton(onPressed: () {}, style: FilledButton.styleFrom(minimumSize: const Size.fromHeight(56)), child: const Text('Assinar Anual R\$99 - 58% OFF')),
            const SizedBox(height: 12),
            OutlinedButton(onPressed: () => Navigator.pop(c), style: OutlinedButton.styleFrom(minimumSize: const Size.fromHeight(48)), child: const Text('Continuar Free')),
          ],
        ),
      ),
    );
  }
}
