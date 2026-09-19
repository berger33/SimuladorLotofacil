import 'package:flutter/material.dart';
import 'package:hive_flutter/hive_flutter.dart';
import '../../../core/constants/colors.dart';
import '../../../core/constants/strings.dart';

class ConfigScreen extends StatelessWidget {
  const ConfigScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Configurações')),
      body: ListView(
        children: [
          const SizedBox(height: 8),
          ListTile(
            leading: const Icon(Icons.palette),
            title: const Text('Tema'),
            subtitle: const Text('Escuro (Material 3)'),
            trailing: const Icon(Icons.chevron_right),
            onTap: () {},
          ),
          ListTile(
            leading: const Icon(Icons.language),
            title: const Text('Idioma'),
            subtitle: const Text('Português (BR)'),
            trailing: const Icon(Icons.chevron_right),
            onTap: () {},
          ),
          ListTile(
            leading: const Icon(Icons.account_balance_wallet),
            title: const Text('Gestão de Banca'),
            subtitle: const Text('R\$ 1000 • Alerta drawdown 50%'),
            trailing: const Icon(Icons.chevron_right),
            onTap: () {},
          ),
          ListTile(
            leading: const Icon(Icons.notifications),
            title: const Text('Notificações'),
            subtitle: const Text('Novos sorteios, novo top'),
            trailing: Switch(value: false, onChanged: (_) {}),
          ),
          const Divider(),
          ListTile(
            leading: const Icon(Icons.workspace_premium, color: AppColors.tertiary),
            title: const Text('Premium'),
            subtitle: const Text('Gerencie assinatura'),
            trailing: const Icon(Icons.chevron_right),
            onTap: () {},
          ),
          ListTile(
            leading: const Icon(Icons.ad_units),
            title: const Text('Remover Anúncios'),
            subtitle: const Text('Assine Pro para remover'),
            trailing: const Icon(Icons.chevron_right),
            onTap: () {},
          ),
          const Divider(),
          ListTile(
            leading: const Icon(Icons.privacy_tip),
            title: const Text('Privacidade'),
            onTap: () => _showPrivacy(context),
          ),
          ListTile(
            leading: const Icon(Icons.description),
            title: const Text('Termos de Uso'),
            onTap: () {},
          ),
          ListTile(
            leading: const Icon(Icons.info),
            title: const Text('Sobre'),
            subtitle: const Text('Lotofácil Pro 1.0.0 • Ferramenta educacional'),
            onTap: () => _showAbout(context),
          ),
          ListTile(
            leading: const Icon(Icons.star_rate, color: AppColors.tertiary),
            title: const Text('Avaliar App'),
            subtitle: const Text('Ajude com 5 estrelas'),
            onTap: () {},
          ),
          ListTile(
            leading: const Icon(Icons.email),
            title: const Text('Contato / Suporte'),
            subtitle: const Text('suporte@lotofacilpro.com'),
            onTap: () {},
          ),
          const Divider(),
          ListTile(
            leading: const Icon(Icons.delete_forever, color: AppColors.error),
            title: const Text('Deletar Dados', style: TextStyle(color: AppColors.error)),
            subtitle: const Text('Apaga ranking e configurações'),
            onTap: () => _confirmDelete(context),
          ),
          const SizedBox(height: 16),
          Padding(
            padding: const EdgeInsets.all(16),
            child: Text(AppStrings.disclaimer, style: const TextStyle(fontSize: 10, color: Colors.grey)),
          ),
          const SizedBox(height: 32),
        ],
      ),
    );
  }

  void _showPrivacy(BuildContext context) {
    showDialog(context: context, builder: (c) => AlertDialog(
      title: const Text('Privacidade'),
      content: const SingleChildScrollView(child: Text(
        'Coletamos: ID dispositivo para ads, analytics anonimizado, crash logs.\n\n'
        'Não coletamos: nome, email, localização.\n\n'
        'Compartilhamos com Google Firebase e AdMob.\n\n'
        'Você pode deletar dados em Configurações > Deletar Dados.\n\n'
        'Completo em: github.com/berger33/SimuladorLotofacil/blob/Aplicativo/android_app/playstore/privacy_policy.md',
      )),
      actions: [TextButton(onPressed: () => Navigator.pop(c), child: const Text('Fechar'))],
    ));
  }

  void _showAbout(BuildContext context) {
    showAboutDialog(
      context: context,
      applicationName: 'Lotofácil Pro',
      applicationVersion: '1.0.0 (Aplicativo)',
      applicationLegalese: 'Ferramenta educacional de simulação estatística.\nNão afiliada à Caixa.\n+18 Jogue com responsabilidade.',
      children: [
        const SizedBox(height: 16),
        const Text('Desenvolvido com ☕ e IA Avançada\nBaseado em Algoritmo Genético + XGBoost + Markov'),
      ],
    );
  }

  void _confirmDelete(BuildContext context) {
    showDialog(context: context, builder: (c) => AlertDialog(
      title: const Text('Deletar tudo?'),
      content: const Text('Isso apaga ranking, favoritos e configurações. Irreversível.'),
      actions: [
        TextButton(onPressed: () => Navigator.pop(c), child: const Text('Cancelar')),
        FilledButton(
          style: FilledButton.styleFrom(backgroundColor: AppColors.error),
          onPressed: () async {
            var box = Hive.box('ranking');
            await box.clear();
            var settings = Hive.box('settings');
            await settings.clear();
            Navigator.pop(c);
            ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Dados deletados')));
          },
          child: const Text('Deletar'),
        ),
      ],
    ));
  }
}
