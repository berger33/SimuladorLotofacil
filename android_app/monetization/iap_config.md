# IAP Config - Google Play Billing

## Play Console > Monetização > Produtos

### Assinaturas
1. lotofacil_pro_monthly
   - Nome: Pro Mensal
   - Descrição: Acesso completo por 1 mês
   - Preço: R$19,90/mês
   - Período: 1 mês
   - Trial: não
   - Grupo: pro_subscription

2. lotofacil_pro_yearly
   - Nome: Pro Anual - Mais Popular
   - Descrição: Acesso completo por 1 ano, 58% OFF
   - Preço: R$99,90/ano
   - Período: 1 ano
   - Trial: 3 dias grátis
   - Grupo: pro_subscription
   - Benefício: anual é upgrade do mensal

### Produto único (não consumível)
3. lotofacil_pro_lifetime
   - Nome: Pro Vitalício
   - Descrição: Pagamento único, acesso para sempre
   - Preço: R$199,90
   - Tipo: não consumível

## Validação servidor
Backend FastAPI endpoint /api/v1/billing/validate
- Recebe purchaseToken
- Valida com Google Play Developer API
- Salva em Firestore users/{uid}/premiumUntil

## Teste
- Licença teste no Play Console > Config > Teste de licença
- Adicionar emails testers
- Usar cartões teste: https://developer.android.com/google/play/billing/test

## Flutter
Usar in_app_purchase, implementar IAPService
