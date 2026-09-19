import 'package:flutter/material.dart';
import '../../../core/constants/colors.dart';
import '../../../data/datasources/local_datasource.dart';

class PremiumScreen extends StatefulWidget {
  const PremiumScreen({super.key});

  @override
  State<PremiumScreen> createState() => _PremiumScreenState();
}

class _PremiumScreenState extends State<PremiumScreen> {
  bool isPremium = false;

  @override
  void initState() {
    super.initState();
    _checkPremium();
  }

  Future<void> _checkPremium() async {
    var premium = await LocalDataSource().isPremium() as bool? ?? false;
    // Hive.box returns directly
    try {
      var box = await Future.value(true); // placeholder
      setState(() {
        isPremium = premium;
      });
    } catch (_) {}
  }

  @override
  Widget build(BuildContext context) {
    if (isPremium) {
      return _buildPremiumActive();
    }
    return _buildPaywall();
  }

  Widget _buildPremiumActive() {
    return Scaffold(
      appBar: AppBar(title: const Text('Premium')),
      body: ListView(
        padding: const EdgeInsets.all(24),
        children: [
          Card(
            color: AppColors.success.withOpacity(0.15),
            child: Padding(
              padding: const EdgeInsets.all(24),
              child: Column(
                children: [
                  const Icon(Icons.workspace_premium, size: 64, color: AppColors.success),
                  const SizedBox(height: 16),
                  Text('Você é Pro! 🎉', style: Theme.of(context).textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.bold, color: AppColors.success)),
                  const SizedBox(height: 8),
                  const Text('Acesso completo desbloqueado', textAlign: TextAlign.center),
                ],
              ),
            ),
          ),
          const SizedBox(height: 24),
          const ListTile(leading: Icon(Icons.check_circle, color: AppColors.success), title: Text('33 jogos'), subtitle: Text('Desbloqueado')),
          const ListTile(leading: Icon(Icons.check_circle, color: AppColors.success), title: Text('IA completa'), subtitle: Text('Ensemble, Apriori, Auto-Piloto, RL')),
          const ListTile(leading: Icon(Icons.check_circle, color: AppColors.success), title: Text('Sem anúncios'), subtitle: Text('Experiência limpa')),
          const ListTile(leading: Icon(Icons.check_circle, color: AppColors.success), title: Text('Export + Suporte VIP'), subtitle: Text('CSV/PDF e WhatsApp sem marca')),
        ],
      ),
    );
  }

  Widget _buildPaywall() {
    return Scaffold(
      body: CustomScrollView(
        slivers: [
          SliverAppBar(
            expandedHeight: 200,
            pinned: true,
            flexibleSpace: FlexibleSpaceBar(
              background: Container(
                decoration: const BoxDecoration(gradient: AppColors.gradientGold),
                child: const Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(Icons.workspace_premium, size: 64, color: Colors.white),
                      SizedBox(height: 8),
                      Text('Lotofácil Pro Premium', style: TextStyle(color: Colors.white, fontSize: 22, fontWeight: FontWeight.bold)),
                      Text('Desbloqueie o potencial máximo', style: TextStyle(color: Colors.white70)),
                    ],
                  ),
                ),
              ),
            ),
          ),
          SliverList(
            delegate: SliverChildListDelegate([
              Padding(
                padding: const EdgeInsets.all(20),
                child: Column(
                  children: [
                    // Comparativo
                    Card(
                      child: Padding(
                        padding: const EdgeInsets.all(16),
                        child: Column(
                          children: [
                            Row(
                              children: [
                                const Expanded(child: Text('Recurso', style: TextStyle(fontWeight: FontWeight.bold))),
                                const SizedBox(width: 40, child: Text('Free', textAlign: TextAlign.center, style: TextStyle(fontWeight: FontWeight.bold))),
                                SizedBox(width: 60, child: Text('Pro', textAlign: TextAlign.center, style: TextStyle(fontWeight: FontWeight.bold, color: AppColors.tertiary))),
                              ],
                            ),
                            const Divider(),
                            _comparativoRow('Qtd Jogos', '10', '33'),
                            _comparativoRow('Gerações', '50', 'Ilimitado'),
                            _comparativoRow('Atrasômetro', '✅', '✅'),
                            _comparativoRow('Markov', '✅', '✅'),
                            _comparativoRow('Ensemble Jedi', '❌', '✅'),
                            _comparativoRow('Apriori Ouro', '❌', '✅'),
                            _comparativoRow('Auto-Piloto', '❌', '✅'),
                            _comparativoRow('RL Autônomo', '❌', '✅'),
                            _comparativoRow('Anúncios', 'Sim', 'Não'),
                            _comparativoRow('Export', '❌', '✅'),
                            _comparativoRow('Turbo', '❌', '✅'),
                          ],
                        ),
                      ),
                    ),
                    const SizedBox(height: 20),

                    // Depoimentos
                    Card(
                      color: AppColors.primary.withOpacity(0.05),
                      child: Padding(
                        padding: const EdgeInsets.all(16),
                        child: Column(
                          children: [
                            const Icon(Icons.format_quote, color: AppColors.primary),
                            const Text('"O ensemble acertou 14 pontos 3x no mês! Vale cada centavo."', style: TextStyle(fontStyle: FontStyle.italic), textAlign: TextAlign.center),
                            const SizedBox(height: 8),
                            const Text('- João, usuário Pro desde 2025', style: TextStyle(fontSize: 12, color: Colors.grey)),
                          ],
                        ),
                      ),
                    ),
                    const SizedBox(height: 20),

                    // Preços
                    _priceCard(
                      title: 'Anual - MAIS POPULAR',
                      price: 'R\$ 99,90',
                      period: '/ano • R\$ 8,32/mês',
                      discount: '58% OFF',
                      features: '3 dias grátis • Cancele quando quiser',
                      isPopular: true,
                      onTap: () => _comprar('anual'),
                    ),
                    const SizedBox(height: 12),
                    _priceCard(
                      title: 'Mensal',
                      price: 'R\$ 19,90',
                      period: '/mês',
                      discount: '',
                      features: 'Flexível mês a mês',
                      isPopular: false,
                      onTap: () => _comprar('mensal'),
                    ),
                    const SizedBox(height: 12),
                    _priceCard(
                      title: 'Vitalício',
                      price: 'R\$ 199,90',
                      period: '• Pagamento único',
                      discount: 'Melhor valor',
                      features: 'Pague uma vez, use para sempre',
                      isPopular: false,
                      onTap: () => _comprar('vitalicio'),
                    ),
                    const SizedBox(height: 24),

                    FilledButton(
                      onPressed: () => _comprar('anual'),
                      style: FilledButton.styleFrom(backgroundColor: AppColors.primary, minimumSize: const Size.fromHeight(56)),
                      child: const Text('Começar 3 dias grátis • Anual R\$99', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                    ),
                    const SizedBox(height: 12),
                    const Text('Cancele a qualquer momento. Sem pegadinhas.', style: TextStyle(fontSize: 11, color: Colors.grey), textAlign: TextAlign.center),
                    const SizedBox(height: 16),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        TextButton(onPressed: () {}, child: const Text('Restaurar compras')),
                        const Text('•'),
                        TextButton(onPressed: () {}, child: const Text('Termos')),
                        const Text('•'),
                        TextButton(onPressed: () {}, child: const Text('Privacidade')),
                      ],
                    ),
                    const SizedBox(height: 32),
                  ],
                ),
              ),
            ]),
          ),
        ],
      ),
    );
  }

  Widget _comparativoRow(String recurso, String free, String pro) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        children: [
          Expanded(child: Text(recurso, style: const TextStyle(fontSize: 13))),
          SizedBox(width: 40, child: Text(free, textAlign: TextAlign.center, style: const TextStyle(fontSize: 13))),
          SizedBox(width: 60, child: Text(pro, textAlign: TextAlign.center, style: TextStyle(fontSize: 13, fontWeight: FontWeight.bold, color: pro == '✅' || pro == '33' || pro.contains('Ilimitado') || pro == 'Não' ? AppColors.success : null))),
        ],
      ),
    );
  }

  Widget _priceCard({required String title, required String price, required String period, required String discount, required String features, required bool isPopular, required VoidCallback onTap}) {
    return Card(
      elevation: isPopular ? 4 : 1,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
        side: isPopular ? const BorderSide(color: AppColors.tertiary, width: 2) : BorderSide.none,
      ),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(16),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Expanded(child: Text(title, style: TextStyle(fontWeight: FontWeight.bold, color: isPopular ? AppColors.tertiary : null))),
                  if (discount.isNotEmpty)
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                      decoration: BoxDecoration(color: AppColors.success, borderRadius: BorderRadius.circular(8)),
                      child: Text(discount, style: const TextStyle(color: Colors.white, fontSize: 10, fontWeight: FontWeight.bold)),
                    ),
                ],
              ),
              const SizedBox(height: 4),
              Row(
                children: [
                  Text(price, style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
                  Text(period, style: const TextStyle(fontSize: 12, color: Colors.grey)),
                ],
              ),
              const SizedBox(height: 4),
              Text(features, style: const TextStyle(fontSize: 11, color: Colors.grey)),
            ],
          ),
        ),
      ),
    );
  }

  void _comprar(String tipo) {
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Compra $tipo - Integração Play Billing em produção')));
  }
}
