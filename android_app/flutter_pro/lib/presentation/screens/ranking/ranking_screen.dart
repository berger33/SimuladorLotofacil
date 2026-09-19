import 'package:flutter/material.dart';
import 'package:share_plus/share_plus.dart';
import '../../../core/constants/colors.dart';
import '../../../domain/entities/matriz.dart';
import '../../../data/datasources/local_datasource.dart';
import '../../widgets/card_matriz.dart';

class RankingScreen extends StatefulWidget {
  const RankingScreen({super.key});

  @override
  State<RankingScreen> createState() => _RankingScreenState();
}

class _RankingScreenState extends State<RankingScreen> with SingleTickerProviderStateMixin {
  late TabController _tabController;
  List<Matriz> ranking = [];
  List<Matriz> favoritos = [];
  int ecossistema = 10;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 3, vsync: this);
    _carregarRanking();
  }

  Future<void> _carregarRanking() async {
    var local = LocalDataSource();
    var dados = await local.getRanking(limit: 50);
    setState(() {
      ranking = dados;
      favoritos = dados.where((m) => m.favorita).toList();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Ranking'),
        bottom: TabBar(
          controller: _tabController,
          tabs: const [
            Tab(text: 'Top 50', icon: Icon(Icons.emoji_events)),
            Tab(text: 'Top 3', icon: Icon(Icons.workspace_premium)),
            Tab(text: 'Favoritos', icon: Icon(Icons.star)),
          ],
        ),
        actions: [
          PopupMenuButton<int>(
            initialValue: ecossistema,
            onSelected: (v) => setState(() => ecossistema = v),
            itemBuilder: (c) => [
              const PopupMenuItem(value: 10, child: Text('Eco 10 jogos')),
              const PopupMenuItem(value: 15, child: Text('Eco 15 jogos')),
              const PopupMenuItem(value: 20, child: Text('Eco 20 jogos')),
              const PopupMenuItem(value: 33, child: Text('Eco 33 jogos (Pro)')),
            ],
            child: Padding(
              padding: const EdgeInsets.all(12),
              child: Row(children: [Text('Eco $ecossistema'), const Icon(Icons.arrow_drop_down)]),
            ),
          ),
          IconButton(icon: const Icon(Icons.refresh), onPressed: _carregarRanking),
        ],
      ),
      body: TabBarView(
        controller: _tabController,
        children: [
          _buildTop50(),
          _buildTop3(),
          _buildFavoritos(),
        ],
      ),
    );
  }

  Widget _buildTop50() {
    if (ranking.isEmpty) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.emoji_events_outlined, size: 64, color: Colors.grey),
            const SizedBox(height: 16),
            const Text('Nenhuma matriz ainda'),
            const Text('Gere no Gerador para ver aqui', style: TextStyle(color: Colors.grey)),
            const SizedBox(height: 16),
            FilledButton.icon(onPressed: () {}, icon: const Icon(Icons.auto_fix_high), label: const Text('Gerar Agora')),
          ],
        ),
      );
    }

    return RefreshIndicator(
      onRefresh: _carregarRanking,
      child: ListView.builder(
        padding: const EdgeInsets.all(12),
        itemCount: ranking.length,
        itemBuilder: (context, i) {
          var matriz = ranking[i];
          return CardMatriz(
            matriz: matriz,
            posicao: i + 1,
            onTap: () => _abrirDetalhes(matriz, i + 1),
            onDelete: () => _deletar(matriz),
            onFavorite: () => _favoritar(matriz),
          );
        },
      ),
    );
  }

  Widget _buildTop3() {
    var top3 = ranking.take(3).toList();
    if (top3.isEmpty) {
      return const Center(child: Text('Gere matrizes para ver Top 3'));
    }

    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        Card(
          color: AppColors.tertiary.withOpacity(0.15),
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              children: [
                const Icon(Icons.emoji_events, size: 48, color: AppColors.tertiary),
                const SizedBox(height: 8),
                Text('🏆 Top 3 Matrizes - Eco $ecossistema jogos', style: Theme.of(context).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.bold)),
                const SizedBox(height: 4),
                const Text('As melhores matrizes por saldo', style: TextStyle(color: Colors.grey)),
              ],
            ),
          ),
        ),
        const SizedBox(height: 16),
        ...top3.asMap().entries.map((e) {
          int idx = e.key;
          var matriz = e.value;
          return Card(
            elevation: 4,
            color: idx == 0 ? AppColors.tertiary.withOpacity(0.1) : null,
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      CircleAvatar(backgroundColor: _getRankColor(idx + 1), child: Text('${idx + 1}', style: const TextStyle(color: Colors.white))),
                      const SizedBox(width: 12),
                      Text('R\$ ${matriz.score.toStringAsFixed(2)}', style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                      const Spacer(),
                      IconButton(icon: const Icon(Icons.share), onPressed: () => _compartilhar(matriz)),
                    ],
                  ),
                  const SizedBox(height: 8),
                  Text('Base 20: ${matriz.base20.map((n) => n.toString().padLeft(2, '0')).join(' ')}', style: const TextStyle(fontFamily: 'monospace')),
                  const SizedBox(height: 8),
                  Text('11:${matriz.stats.h11} 12:${matriz.stats.h12} 13:${matriz.stats.h13} 14:${matriz.stats.h14} 15:${matriz.stats.h15}'),
                  const SizedBox(height: 8),
                  FilledButton(onPressed: () => _abrirDetalhes(matriz, idx + 1), child: const Text('Ver Detalhes')),
                ],
              ),
            ),
          );
        }),
      ],
    );
  }

  Widget _buildFavoritos() {
    if (favoritos.isEmpty) {
      return const Center(child: Text('Nenhuma favorita ainda\nFavorite matrizes no Top 50', textAlign: TextAlign.center));
    }
    return ListView.builder(
      padding: const EdgeInsets.all(12),
      itemCount: favoritos.length,
      itemBuilder: (c, i) => CardMatriz(matriz: favoritos[i], posicao: i + 1, onTap: () => _abrirDetalhes(favoritos[i], i + 1)),
    );
  }

  Color _getRankColor(int pos) {
    if (pos == 1) return AppColors.tertiary;
    if (pos == 2) return Colors.grey;
    if (pos == 3) return const Color(0xFFCD7F32);
    return AppColors.primary;
  }

  void _abrirDetalhes(Matriz matriz, int pos) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(24))),
      builder: (c) => DraggableScrollableSheet(
        initialChildSize: 0.8,
        maxChildSize: 0.95,
        minChildSize: 0.5,
        expand: false,
        builder: (context, scrollController) => ListView(
          controller: scrollController,
          padding: const EdgeInsets.all(20),
          children: [
            Center(child: Container(width: 40, height: 4, decoration: BoxDecoration(color: Colors.grey[600], borderRadius: BorderRadius.circular(2)))),
            const SizedBox(height: 16),
            Row(
              children: [
                CircleAvatar(backgroundColor: _getRankColor(pos), radius: 24, child: Text('$pos', style: const TextStyle(color: Colors.white, fontSize: 18))),
                const SizedBox(width: 12),
                Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Text('Posição $pos • R\$ ${matriz.score.toStringAsFixed(2)}', style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                  Text('G${matriz.geracao} • ${matriz.qtdJogos} jogos • ${matriz.timestamp.day}/${matriz.timestamp.month}'),
                ])),
                IconButton(icon: const Icon(Icons.star, color: AppColors.tertiary), onPressed: () => _favoritar(matriz)),
              ],
            ),
            const SizedBox(height: 16),
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(color: AppColors.primary.withOpacity(0.1), borderRadius: BorderRadius.circular(12)),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text('⭐ 20 Dezenas de Ouro', style: TextStyle(fontWeight: FontWeight.bold)),
                  const SizedBox(height: 8),
                  Text(matriz.base20.map((n) => n.toString().padLeft(2, '0')).join(' '), style: const TextStyle(fontFamily: 'monospace', fontSize: 16, fontWeight: FontWeight.bold)),
                ],
              ),
            ),
            const SizedBox(height: 16),
            Row(
              children: [
                _statChip('11', matriz.stats.h11, Colors.grey),
                const SizedBox(width: 6),
                _statChip('12', matriz.stats.h12, Colors.blueGrey),
                const SizedBox(width: 6),
                _statChip('13', matriz.stats.h13, Colors.blue),
                const SizedBox(width: 6),
                _statChip('14', matriz.stats.h14, AppColors.warning),
                const SizedBox(width: 6),
                _statChip('15', matriz.stats.h15, AppColors.success),
              ],
            ),
            const SizedBox(height: 16),
            Text('🎯 Rede de Sinergia (${matriz.sistema.length} jogos)', style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            ...matriz.sistema.asMap().entries.map((e) => Card(
              child: ListTile(
                dense: true,
                title: Text('Aposta ${e.key+1}: ${e.value.map((n) => n.toString().padLeft(2, '0')).join(' ')}', style: const TextStyle(fontFamily: 'monospace', fontSize: 12)),
                trailing: IconButton(icon: const Icon(Icons.copy, size: 18), onPressed: () {}),
              ),
            )),
            const SizedBox(height: 16),
            Text('🧪 Stress Tests', style: Theme.of(context).textTheme.titleMedium),
            const SizedBox(height: 8),
            Row(
              children: [
                Expanded(child: OutlinedButton.icon(onPressed: () => _stressTest(matriz, 'historico'), icon: const Icon(Icons.history), label: const Text('Histórico'))),
                const SizedBox(width: 8),
                Expanded(child: OutlinedButton.icon(onPressed: () => _stressTest(matriz, 'caos'), icon: const Icon(Icons.shuffle), label: const Text('Caos 100k'))),
              ],
            ),
            const SizedBox(height: 8),
            FilledButton.icon(onPressed: () => _compartilhar(matriz), icon: const Icon(Icons.share), label: const Text('Compartilhar WhatsApp'), style: FilledButton.styleFrom(minimumSize: const Size.fromHeight(48))),
            const SizedBox(height: 8),
            OutlinedButton.icon(onPressed: () {}, icon: const Icon(Icons.download), label: const Text('Exportar CSV/PDF (Pro)')),
          ],
        ),
      ),
    );
  }

  Widget _statChip(String label, int value, Color color) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 8),
        decoration: BoxDecoration(color: color.withOpacity(0.15), borderRadius: BorderRadius.circular(8), border: Border.all(color: color.withOpacity(0.3))),
        child: Column(children: [
          Text(label, style: TextStyle(fontSize: 10, color: color, fontWeight: FontWeight.bold)),
          Text('$value', style: TextStyle(fontWeight: FontWeight.bold, color: color)),
        ]),
      ),
    );
  }

  void _deletar(Matriz matriz) {
    showDialog(context: context, builder: (c) => AlertDialog(
      title: const Text('Deletar matriz?'),
      content: Text('Deletar matriz R\$ ${matriz.score.toStringAsFixed(2)}?'),
      actions: [
        TextButton(onPressed: () => Navigator.pop(c), child: const Text('Cancelar')),
        FilledButton(onPressed: () async {
          await LocalDataSource().deletarMatriz(matriz.id);
          Navigator.pop(c);
          _carregarRanking();
        }, child: const Text('Deletar')),
      ],
    ));
  }

  void _favoritar(Matriz matriz) async {
    await LocalDataSource().favoritarMatriz(matriz.id, !matriz.favorita);
    _carregarRanking();
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(matriz.favorita ? 'Removido dos favoritos' : 'Adicionado aos favoritos')));
  }

  void _compartilhar(Matriz matriz) {
    var texto = '🎰 Lotofácil Pro - Matriz Top\nR\$ ${matriz.score.toStringAsFixed(2)}\nBase 20: ${matriz.base20.map((n) => n.toString().padLeft(2, '0')).join(' ')}\n\nGerado com Lotofácil Pro App\nhttps://play.google.com/store/apps/details?id=com.berger33.lotofacilpro';
    Share.share(texto);
  }

  void _stressTest(Matriz matriz, String tipo) {
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('🧪 Stress $tipo iniciado... (Pro libera 3 tipos)')));
  }
}
