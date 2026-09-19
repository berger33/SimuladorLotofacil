# AdMob Config

## Criar conta
https://admob.google.com

## App ID (no AndroidManifest.xml)
<meta-data android:name="com.google.android.gms.ads.APPLICATION_ID" android:value="ca-app-pub-3940256099942544~3347511713"/> <!-- teste -->

## Unidades de anúncio (produção trocar)

### Banner Dashboard
- ID: ca-app-pub-3940256099942544/6300978111 (teste)
- Produção: criar no AdMob > Banner > lotofacil_dashboard_banner
- Tamanho: BANNER ou ADAPTIVE_BANNER
- Refresh: 30s

### Interstitial Geração
- ID teste: ca-app-pub-3940256099942544/1033173712
- Produção: lotofacil_interstitial_geracao
- Frequência: a cada 3 gerações

### Rewarded +20 Gerações
- ID teste: ca-app-pub-3940256099942544/5224354917
- Produção: lotofacil_rewarded_extra

## Código Flutter
Ver docs/MONETIZACAO_PLAYSTORE.md

## Políticas
- Não clicar próprio anúncio
- Não incentivar clique acidental (botão perto)
- Não mostrar interstitial ao sair do app
- Respeitar GDPR, mostrar consent form se EU
